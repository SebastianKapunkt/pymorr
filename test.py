import pymorr


def run():
    p = pymorr.Pymorr()
    p.set_root('/Users/devbook/Downloads/Keep/')
    pictures = p.get_image_paths_from_root()
    for picture in pictures:
        p.move_image(picture, p.prefered_folder['Keep'])
        p.undo_last_move()

def show_log_images_paths():
    p = pymorr.Pymorr()
    p.set_root('/Users/devbook/Downloads/Keep/')
    print(p.get_image_paths_from_log())

def show_image_paths_from_root():
    p = pymorr.Pymorr()
    p.set_root('/Users/devbook/Downloads/Keep/')
    print(p.get_image_paths_from_root())

if __name__ == '__main__':
    run()
    show_log_images_paths()
    show_image_paths_from_root()
