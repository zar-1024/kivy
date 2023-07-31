import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from openpyxl import load_workbook

wb = load_workbook("orders.xlsx")
sheet_1 = wb['active_tables']
sheet_2 = wb['todays_orders']

class AddOrders(Widget):
    order_type_list = ["Hot", "Cold", "Food"]
    order_choice = []
    order_list = []
    var_1 = None

    def table_num_input(self):
        table_num = self.ids.tab_num.text
        table_num = table_num.zfill(2)
        now = datetime.datetime.now()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
        if table_num != "00":
            self.ids.show_table_num.text = f'Table Number: {table_num}'
        if table_num != "00":
            self.order_list.append(table_num)
            self.order_list.append(timestamp)
            self.ids.tab_num.text = ""
            self.ids.tab_num.disabled = True

    def order_type(self, value):
        global order_choice
        match value:
            case "Hot":
                order_choice = ["3 in 1", "coffee", "tea"]
                self.ids.order_id.values = order_choice

            case "Cold":
                order_choice = ["ice 3 in 1", "ice coffee", "ice tea"]
                self.ids.order_id.values = order_choice

            case "Food":
                order_choice = ["4 cheese", "hot dog"]
                self.ids.order_id.values = order_choice


    def order_choice(self, value):
        global var_1
        var_1 = value

    def order_save(self):
        global var_1
        self.order_list.append(var_1)
        var_1 = None
        self.ids.order_type_id.text = "Select Order Type"
        self.ids.order_id.text = "Select Order"


    def submit_orders(self):
        self.order_list = [x for x in self.order_list if x != "Select Order"]
        self.ids.order_type_id.text = "Select Order Type"
        self.ids.order_id.text = "Select Order"
        self.ids.tab_num.text = ""
        num_rows = sheet_1.max_row
        for i, item in enumerate(self.order_list, start=1):
            sheet_1.cell(row=num_rows + 1, column=i).value = item
        wb.save("orders.xlsx")
        self.order_list = []
        self.ids.tab_num.disabled = False
        self.ids.show_table_num.text = ""


kv = Builder.load_file("cafeorders.kv")


class myApp(App):
    def build(self):
        return AddOrders()


if __name__ == "__main__":
    myApp().run()
