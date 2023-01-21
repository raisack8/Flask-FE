class TestInfo:
    current_select_section=[]
    mode_str = "説明→用語"

    def get_sec(self):
        return self.current_select_section

    def set_sec(self, new_select_section):
        self.current_select_section = new_select_section

    def change_mode(self):
        if(self.mode_str == "説明→用語"):
            self.mode_str = "用語→説明"
        else:
            self.mode_str = "説明→用語"
    def get_mode(self):
        return self.mode_str