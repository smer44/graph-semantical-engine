


class gCanvasStringItemRenderer:


    def __init__(self):
        pass



    def create_visual_item(self,canvas,item):
        assert isinstance(item.left,(int,float)) and isinstance(item.bottom,(int,float)) and \
               isinstance(item.right,(int,float)) and isinstance(item.top,(int,float))

        rect_id = canvas.create_rectangle(item.left, item.bottom, item.right, item.top, outline='gray', width=2)
        item.rect_id = rect_id
        item.text_id = canvas.create_text((item.left + item.right) / 2, (item.bottom + item.top) / 2,
                                        text=item.value.value)


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

    def move_visual_item(self,canvas,item,dx,dy):
        canvas.move(item.rect_id, dx, dy)
        canvas.move(item.text_id, dx, dy)

    def update_text_on_item(self,canvas, item, text):
        item.value.set(text)
        canvas.itemconfig(item.text_id, text=str(item.value))



