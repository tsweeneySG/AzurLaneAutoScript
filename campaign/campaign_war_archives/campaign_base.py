from module.base.utils import random_rectangle_vector
from module.campaign.campaign_base import CampaignBase as CampaignBase_
from module.exception import RequestHumanTakeover
from module.logger import logger
from module.ui.assets import WAR_ARCHIVES_CHECK
from module.ui.page import page_archives
from module.ui.switch import Switch
from module.war_archives.assets import WAR_ARCHIVES_EX_ON, WAR_ARCHIVES_SP_ON, WAR_ARCHIVES_CAMPAIGN_CHECK
from module.war_archives.dictionary import dic_archives_template

WAR_ARCHIVES_SWITCH = Switch('War_Archives_switch', is_selector=True)
WAR_ARCHIVES_SWITCH.add_status('ex', WAR_ARCHIVES_EX_ON)
WAR_ARCHIVES_SWITCH.add_status('sp', WAR_ARCHIVES_SP_ON)


class CampaignBase(CampaignBase_):
    # Helper variable to keep track of whether is the first runthrough
    first_run = True

    def _get_archives_entrance(self, name):
        """
        Create entrance button to target archive campaign
        using a template acquired by event folder name

        Args:
            name(str): event folder name
        """
        template = dic_archives_template[name]

        sim, button = template.match_result(self.device.image)
        if sim < 0.85:
            return None

        entrance = button.crop((-12, -12, 44, 32), image=self.device.image, name=name)
        return entrance

    def _search_archives_entrance(self, name, skip_first_screenshot=True):
        """
        Search for entrance using mini-touch scroll down
        at center
        Fixed number of scrolls until give up, may need to
        increase as more war archives campaigns are added
        """
        detection_area = (565, 125, 700, 675)

        for _ in range(10):
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            # Drag may result in accidental exit, recover
            # before starting next search attempt
            while not self.appear(WAR_ARCHIVES_CHECK):
                self.ui_ensure(destination=page_archives)

            entrance = self._get_archives_entrance(name)
            if entrance is not None:
                return entrance

            # backup = self.config.cover(DEVICE_CONTROL_METHOD='minitouch')
            p1, p2 = random_rectangle_vector(
                (0, -275), box=detection_area, random_range=(-50, -50, 50, 50), padding=20)
            self.device.drag(p1, p2, segments=2, shake=(0, 25), point_random=(0, 0, 0, 0), shake_random=(0, -5, 0, 5))
            # backup.recover()
            self.device.sleep(0.3)

        logger.warning('Failed to find archives entrance')
        return None

    def ui_goto_archives_campaign(self, mode='ex'):
        """
        Performs the operations needed to transition
        to target archive's campaign stage map
        """
        # On first run regardless of current location
        # even in target stage map, start from page_archives
        # For subsequent runs when neither reward or
        # stop_triggers occur, no need perform operations
        result = True
        if self.first_run or not self.appear(WAR_ARCHIVES_CAMPAIGN_CHECK, offset=(20, 20)):
            result = self.ui_ensure(destination=page_archives)

            WAR_ARCHIVES_SWITCH.set(mode, main=self)

            entrance = self._search_archives_entrance(self.config.Campaign_Event)
            if entrance is not None:
                self.ui_click(entrance, appear_button=WAR_ARCHIVES_CHECK, check_button=WAR_ARCHIVES_CAMPAIGN_CHECK,
                              skip_first_screenshot=True)
            else:
                logger.critical('Respective server may not yet support the chosen War Archives campaign, '
                                'check back in the next app update')
                raise RequestHumanTakeover

        # Subsequent runs all set False
        if self.first_run:
            self.first_run = False

        return result

    def ui_goto_event(self):
        """
        Overridden to handle specifically transitions
        to target ex event in page_archives
        """
        return self.ui_goto_archives_campaign(mode='ex')

    def ui_goto_sp(self):
        """
        Overridden to handle specifically transitions
        to target sp event in page_archives
        """
        return self.ui_goto_archives_campaign(mode='sp')
