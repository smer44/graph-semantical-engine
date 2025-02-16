from gse.dictgraph import DictGraph
from gse.entitygraph import Entity


class gCanvasClzItemRenderer:


    def __init__(self):
        #self.shown_fields = set(["value"])
        self.header_height = 16



    def __header_and_shown_fields_for_entity__(self,controller,entity):
        #print(f"__header_and_shown_fields_for_entity__ : {entity=}")
        if entity.parent is None:
            header_str = f"{entity.name}"
        else:
            header_str = f"{entity.name} : {entity.parent}"

        snown_fields = [x  for x in controller.gen_field_names_values_for_gui(entity)]
        return header_str, snown_fields


    def __header_and_shown_fields_for_to_str__(self, item):
        header_str =  f"{str(type(item).__name__)} : {item}"
        shown_fields = []
        return header_str,shown_fields


    def __header_and_shown_fields_for_default__(self, item):
        #print(f"__header_and_shown_fields_for_default__ : {item=}")
        header_str = str(type(item).__name__)


        shown_fields =[]
        for k in dir(item):
            if not k.startswith("_"):
                v = getattr(item, k)
                if not callable(v):
                    shown_fields.append((k,str(v)))

        return header_str, shown_fields





    def assert_item_bounds_type(self,item):

        return isinstance(item.left,(int,float)) and isinstance(item.bottom,(int,float)) and \
               isinstance(item.right,(int,float)) and isinstance(item.top,(int,float))

    def create_visual_item(self, canvas,item):
        controller = canvas.controller
        if not hasattr(item, "value"):
            header_str, shown_fields = self.__header_and_shown_fields_for_default__(item)
            header_str+=" !! not inboxed"
        elif isinstance(item.value,Entity):
            header_str, shown_fields = self.__header_and_shown_fields_for_entity__(controller, item.value)
        elif isinstance(item.value,str):
            header_str, shown_fields = self.__header_and_shown_fields_for_to_str__(item.value)
        else:
            header_str, shown_fields = self.__header_and_shown_fields_for_default__(item.value)


        self.__create_visual_item__(canvas,item,header_str, shown_fields)


    def __create_visual_item__(self,canvas,item,header_str, shown_fields):
        assert self.assert_item_bounds_type(item)

        #inboxed_item = item.value
        #Create header
        #header_str = self.get_item_header(inboxed_item)

        #those are estimated, too large coordinates:
        hleft =item.left
        hbot = item.bottom
        hright = item.right
        htop = item.bottom

        #header_rect_id = canvas.create_rectangle(hleft, hbot, hright, htop, outline='gray', width=1)

        #header_line_id = canvas.create_line(hleft, htop, hright, htop,fill='gray', width=1)
        initial_x, initial_y = (hleft + hright) / 2, (hbot + htop) / 2,
        header_text_id = canvas.create_text(initial_x, initial_y,text=header_str,anchor='center')
        header_coords = canvas.bbox(header_text_id)
        xmin,y0,xmax,ymax = header_coords
        ymax+=2
        yheader = ymax


        item.__setattr__("visuals",list())
        #item.visuals.append(header_line_id)
        item.visuals.append(header_text_id)

        lines = []
        for field_name, value in shown_fields:
            line = f"{field_name} : {value}"
            lines.append(line)
        lined_text = "\n".join(lines)
        line_amount = len(lines)
        #body_text_id = canvas.create_line(hleft, htop, hright, htop, fill='gray', width=1)
        body_text_id = canvas.create_text(initial_x, ymax, text=lined_text,anchor='n')
        header_coords = canvas.bbox(body_text_id)
        xmin2, _, xmax2, ymax = header_coords
        xmin = min(xmin,xmin2)
        xmax = max(xmax,xmax2)
        item.visuals.append(body_text_id)
        item.left, item.bottom, item.right, item.top = xmin, y0,xmax,ymax
        rect_id = canvas.create_rectangle(item.left, item.bottom, item.right, item.top, outline='gray', width=2)
        item.rect_id = rect_id
        if line_amount > 0:
            ystep =(ymax - yheader) //(line_amount)
            y1 = yheader
            for line_nr in range(line_amount):
                middle_line = canvas.create_line(item.left+2, y1, item.right-2, y1,fill='gray', width=1)
                item.visuals.append(middle_line)
                y1 = y1+ystep



            #value = getattr(item.value,field_name)
            #field_name_id = canvas.create_text(text_name_x,text_bot, text=field_name)
            #field_value_id = canvas.create_text(text_value_x, text_bot, text=value)
            #line_before_field_id = canvas.create_line(hleft, htop, hright, htop,fill='gray', width=1)
            #item.visuals.append(field_name_id)
            #item.visuals.append(field_value_id)
            #item.visuals.append(line_before_field_id)
            #text_bot =  text_bot+step
            #htop += step



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


    def update_text_on_item(self, canvas, item, text):
        original_graph = canvas.original_graph
        print(f"called {item=} , {text=}")
        old_value = item.value

        if isinstance(item.value, str):
            item.value = text
        else:
            item.value.set(text)
        if isinstance(original_graph, DictGraph):
            original_graph.replace_value(old_value,text)
        else:
            assert False , f" update_text_on_item unfinished for graph type {type(original_graph)}"
        if 2 == len(item.visuals):
            #this is primitive value
            canvas_object_id = item.visuals[0]
            canvas.itemconfig(canvas_object_id, text=str(item.value))
        else:
            assert False, f" update_text_on_item unfinished for item type {type(item.value)} , {item.visuals=}"



