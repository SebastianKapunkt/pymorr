import pymorr


def run():
    p = pymorr.Pymorr()
    p.set_root('/Users/devbook/Downloads/Keep/')
    pictures = p.get_image_paths_from_root()
    for picture in pictures:
        p.move_image(picture,p.prefered_folder['Keep'])
        p.undo_last_move()

if __name__ == '__main__':
    run()
