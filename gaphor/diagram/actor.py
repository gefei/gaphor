'''
ActorItem diagram item
'''
# vim:sw=4

import UML
from modelelement import ModelElementItem
import diacanvas
import pango

class ActorItem(ModelElementItem):
    HEAD=11
    ARM=19
    NECK=10
    BODY=20
    FONT='sans bold 10'

    def __init__(self):
	ModelElementItem.__init__(self)
	self.set(height=(ActorItem.HEAD + ActorItem.NECK + ActorItem.BODY + ActorItem.ARM),
		 width=(ActorItem.ARM * 2))
	self.set(min_height=(ActorItem.HEAD + ActorItem.NECK + ActorItem.BODY + ActorItem.ARM),
		 min_width=(ActorItem.ARM * 2))
	# Head
	self.__head = diacanvas.shape.Ellipse()
	self.__head.set_line_width(2.0)
	# Body
	self.__body = diacanvas.shape.Path()
	self.__body.set_line_width(2.0)
	# Arm
	self.__arms = diacanvas.shape.Path()
	self.__arms.set_line_width(2.0)
	# Legs
	self.__legs = diacanvas.shape.Path()
	self.__legs.set_line_width(2.0)
	# Name
	self.add(diacanvas.CanvasText())
	assert self.__name != None
	font = pango.FontDescription(ActorItem.FONT)
	self.__name.set(font=font, width=self.width,
			alignment=pango.ALIGN_CENTER)
	#self.__name_update()
	# Center the text:
	w, h = self.__name.get_property('layout').get_pixel_size()
	#print 'ActorItem:',w,h
	#self.__name.move(0, self.height)
	self.__name.set(height=h, width=w)
	self.__name.connect_object('text_changed', ActorItem.on_text_changed, self)

    def __name_update (self):
	'''Center the name text under the actor.'''
	w, h = self.__name.get_property('layout').get_pixel_size()
	#print 'ActorItem:',w,h
	#self.set(min_width=w + UseCase.MARGIN_X,
	#	 min_height=h + UseCase.MARGIN_Y)
	a = self.__name.get_property('affine')
	aa = (a[0], a[1], a[2], a[3], w / -2 + ActorItem.ARM, self.height)
	#self.__name.set(affine=aa, width=self.width, height=h)
	if w < self.width:
	    w = self.width
	self.__name.set(affine=aa, width=w, height=h)
	
    def on_update(self, affine):
	ModelElementItem.on_update(self, affine)

	# scaling factors (also compenate the line width):
	fx = self.width / (ActorItem.ARM * 2 - 2);
	fy = self.height / (ActorItem.HEAD + ActorItem.NECK + ActorItem.BODY + ActorItem.ARM - 2);
	self.__head.ellipse((ActorItem.ARM * fx, (ActorItem.HEAD / 2) * fy),
			    ActorItem.HEAD * fx, ActorItem.HEAD * fy)
	self.__head.request_update()
	self.__body.line(((ActorItem.ARM * fx, ActorItem.HEAD * fy),
			 (ActorItem.ARM * fx, (ActorItem.HEAD + ActorItem.NECK + ActorItem.BODY) * fy)))
	self.__body.request_update()
	self.__arms.line(((0, (ActorItem.HEAD + ActorItem.NECK) * fy),
			 (ActorItem.ARM * 2 * fx, (ActorItem.HEAD + ActorItem.NECK) * fy)))
	self.__arms.request_update()
	self.__legs.line(((0, (ActorItem.HEAD + ActorItem.NECK + ActorItem.BODY + ActorItem.ARM) * fy),
			  (ActorItem.ARM * fx, (ActorItem.HEAD + ActorItem.NECK + ActorItem.BODY) * fy),
			  (ActorItem.ARM * 2 * fx, (ActorItem.HEAD + ActorItem.NECK + ActorItem.BODY + ActorItem.ARM) * fy)))
	self.__legs.request_update()
	self.__name.update_now()
	# Update the bounding box:
	ulx, uly, lrx, lry = self.bounds
	w, h = self.__name.get_property('layout').get_pixel_size()
	if w > self.width:
	    ulx = (self.width / 2) - (w / 2)
	    lrx = (self.width / 2) + (w / 2)
	self.set_bounds ((ulx, uly, lrx, lry + h))

    def on_get_shape_iter(self):
	return self.__head

    def on_shape_next(self, iter):
	if iter is self.__head:
	    return self.__body
	elif iter is self.__body:
	    return self.__arms
	elif iter is self.__arms:
	    return self.__legs
	return None

    def on_shape_value(self, iter):
	return iter

    def on_move(self, x, y):
	self.__name.request_update()
	ModelElementItem.on_move(self, x, y)

    def on_handle_motion (self, handle, wx, wy, mask):
	retval  = ModelElementItem.on_handle_motion(self, handle, wx, wy, mask)
	self.__name_update()
	return retval

    # Groupable

    def on_groupable_add(self, item):
	try:
	    if self.__name is not None:
		raise AttributeError, 'No more canvas items should be set'
	except AttributeError:
	    self.__name = item
	    return 1
	return 0

    def on_groupable_remove(self, item):
	'''Do not allow the name to be removed.'''
	self.emit_stop_by_name('remove')
	return 0

    def on_groupable_get_iter(self):
	return self.__name

    def on_groupable_next(self, iter):
	return None

    def on_groupable_value(self, iter):
	return iter

    def on_groupable_length(self):
	return 1

    def on_groupable_pos(self, item):
	if item == self.__name:
	    return 0
	else:
	    return -1

    def on_subject_update(self, name):
	if name == 'name':
	    self.__name.set(text=self.subject.name)
	    self.__name_update()
	else:
	    ModelElementItem.on_subject_update(self, name)

    def on_text_changed(self, text):
	if text != self.subject.name:
	    self.subject.name = text
	    self.__name_update()

import gobject
gobject.type_register(ActorItem)
