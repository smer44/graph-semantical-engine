from gse.entitygraph import Entity


class gCanvasClzItemRenderer:


    def __init__(self):
        #self.shown_fields = set(["value"])
        self.header_height = 16



    def __header_and_shown_fields_for_entity__(self,entity):
        if entity.parent is None:
            header_str = f"{entity.name}"
        else:
            header_str = f"{entity.name} :{entity.parent.name}"

        snown_fields = [x for x in entity.gen_shown_fields()]
        return header_str, snown_fields


    def __header_and_shown_fields_for_default__(self, item):
        header_str = str(type(item).__name__)


        shown_fields =[]
        for k in dir(item):
            if not k.startswith("_"):
                v = getattr(item, k)
                if not callable(v):
                    shown_fields.append((k,v))

        return header_str, shown_fields





    def assert_item_bounds_type(self,item):
        return isinstance(item.left,(int,float)) and isinstance(item.bottom,(int,float)) and \
               isinstance(item.right,(int,float)) and isinstance(item.top,(int,float))

    def create_visual_item(self, canvas,item):
        if not hasattr(item, "value"):
            header_str, shown_fields = self.__header_and_shown_fields_for_default__(item)
            header_str+=" !! not inboxed"
        elif isinstance(item.value,Entity):
            header_str, shown_fields = self.__header_and_shown_fields_for_entity__(item.value)
        else:
            header_str, shown_fields = self.__header_and_shown_fields_for_default__(item.value)


        self.__create_visual_item__(canvas,item,header_str, shown_fields)


    def __create_visual_item__(self,canvas,item,header_str, shown_fields):
        assert self.assert_item_bounds_type(item)

        #inboxed_item = item.value
        #Create header
        #header_str = self.get_item_header(inboxed_item)

        hleft =item.left+1
        hbot = item.bottom+1
        hright = item.right -1
        htop = item.bottom + self.header_height-1

        #header_rect_id = canvas.create_rectangle(hleft, hbot, hright, htop, outline='gray', width=1)

        #header_line_id = canvas.create_line(hleft, htop, hright, htop,fill='gray', width=1)
        header_text_id = canvas.create_text((hleft + hright) / 2, (hbot + htop) / 2,
                                        text=header_str)

        rect_id = canvas.create_rectangle(item.left, item.bottom, item.right, item.top, outline='gray', width=2)
        item.rect_id = rect_id
        htop +=2
        step = (item.top - htop) // len(shown_fields)
        step_half = step//2
        #text_mid_x = (item.left + item.right) // 2
        text_name_x = (item.left + item.left +item.left +item.right) // 4
        text_value_x = (item.left + item.right+ item.right+ item.right) // 4
        text_bot = htop+step_half

        item.__setattr__("visuals",list())
        #item.visuals.append(header_line_id)
        item.visuals.append(header_text_id)

        for field_name, value in shown_fields:
            #value = getattr(item.value,field_name)
            field_name_id = canvas.create_text(text_name_x,text_bot, text=field_name)
            field_value_id = canvas.create_text(text_value_x, text_bot, text=value)
            line_before_field_id = canvas.create_line(hleft, htop, hright, htop,fill='gray', width=1)
            item.visuals.append(field_name_id)
            item.visuals.append(field_value_id)
            item.visuals.append(line_before_field_id)
            text_bot =  text_bot+step
            htop += step


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



