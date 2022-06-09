


class ScraperPage():
    __slots__='name','list_xpaths_to_click','list_xpaths_to_click_scroll','list_xpaths_to_select','list_xpaths_to_select_scroll','list_select_options'

    def __init__(self,name,list_xpaths_to_click=[],list_xpaths_to_click_scroll=[],list_xpaths_to_select=[],list_xpaths_to_select_scroll=[],list_select_options=[]):
        self.name = name
        self.list_xpaths_to_click = list_xpaths_to_click
        self.list_xpaths_to_click_scroll = list_xpaths_to_click_scroll
        self.list_xpaths_to_select = list_xpaths_to_select
        self.list_xpaths_to_select_scroll = list_xpaths_to_select_scroll
        self.list_select_options = list_select_options

    def get_page_name(self):
        return self.name
    
    def get_list_xpaths_to_click(self):
        return self.list_xpaths_to_click
    
    def get_list_xpaths_to_click_scroll(self):
        return self.list_xpaths_to_click_scroll
    
    def get_list_xpaths_to_select(self):
        return self.list_xpaths_to_select
    
    def get_list_xpaths_to_select_scroll(self):
        return self.list_xpaths_to_select_scroll
    
    def get_list_select_options(self):
        return self.list_select_options