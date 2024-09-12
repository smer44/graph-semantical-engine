


class gCanvasClzItemRenderer:


    def __init__(self):
        self.shown_fields = set(["value"])
        self.header_height = 16


    def get_item_header(self,item):
        return str(type(item).__name__)




    def create_visual_item(self,canvas,item):
        assert isinstance(item.left,(int,float)) and isinstance(item.bottom,(int,float)) and \
               isinstance(item.right,(int,float)) and isinstance(item.top,(int,float))

        inboxed_item = item.value
        #Create header
        header_str = self.get_item_header(inboxed_item)

        hleft =item.left+1
        hbot = item.bottom+1
        hright = item.right -1
        htop = item.bottom + self.header_height-1

        header_rect_id = canvas.create_rectangle(hleft, hbot, hright, htop, outline='gray', width=1)
        header_text_id = canvas.create_text((hleft + hright) / 2, (hbot + htop) / 2,
                                        text=header_str)

        rect_id = canvas.create_rectangle(item.left, item.bottom, item.right, item.top, outline='gray', width=2)
        item.rect_id = rect_id

        step = (htop - item.bottom) // len(self.shown_fields)
        step_half = step//2
        text_mid_x = (item.left + item.right) // 2
        text_name_x = (item.left + item.left +item.left +item.right) // 4
        text_value_x = (item.left + item.right+ item.right+ item.right) // 4
        text_bot = htop+step_half

        item.__setattr__("visuals",list())
        item.visuals.append(header_rect_id)
        item.visuals.append(header_text_id)

        for field_name in self.shown_fields:
            value = getattr(item.value,field_name)
            field_name_id = canvas.create_text(text_name_x,text_bot, text=field_name)
            field_value_id = canvas.create_text(text_value_x, text_bot, text=value)
            item.visuals.append(field_name_id)
            item.visuals.append(field_value_id)
            text_bot =  text_bot+step


    def update_color(self,canvas, item, is_selected,is_selected_for_connect):
        if is_selected:
            if is_selected_for_connect:
                color = "purple"
            else:
                color = "blue"
        else:
            if is_selected_for_connect:
                color = "red"
            else:
                color = "gray"
        canvas.itemconfig(item.rect_id, outline=color)

    def delete_visual_item(self,canvas, item):
        canvas.delete(item.rect_id)
        canvas.delete(item.text_id)
        if item.visuals:
            for visual_item in item.visuals:
                canvas.delete(visual_item)
                canvas.delete(visual_item)

    def move_visual_item(self,canvas,item,dx,dy):
        canvas.move(item.rect_id, dx, dy)
        #canvas.move(item.text_id, dx, dy)
        if item.visuals:
            for visual_item in item.visuals:
                canvas.move(visual_item,dx,dy)


    def update_text_on_item(self,canvas, item, text):
        item.value.set(text)
        canvas.itemconfig(item.text_id, text=str(item.value))



