from pivy import coin
from pivy.utils import get_point_on_screen
from .colors import COLORS
from .plot import plot
from .mesh import simple_quad_mesh, simple_poly_mesh


class Object3D(coin.SoSeparator):
    std_col = "black"
    ovr_col = "red"
    sel_col = "yellow"
    non_col = "grey"

    def __init__(self, points, dynamic=False):
        super(Object3D, self).__init__()
        self.data = coin.SoCoordinate3()
        self.color = coin.SoMaterial()
        self.set_color()
        self += [self.color, self.data]
        self.start_pos = None
        self.dynamic = dynamic

        # callback function lists
        self.on_drag = []
        self.on_drag_release = []
        self.on_drag_start = []

        self._delete = False
        self._tmp_points = None
        self.enabled = True
        self.points = points

    def set_disabled(self):
        self.color.diffuseColor = COLORS[self.non_col]
        self.enabled = False

    def set_enabled(self):
        self.color.diffuseColor = COLORS[self.std_col]
        self.enabled = True

    def set_color(self, col=None):
        self.std_col = col or self.std_col
        self.color.diffuseColor = COLORS[self.std_col]

    @property
    def points(self):
        return self.data.point.getValues()

    @points.setter
    def points(self, points):
        # check if we got a list of 3D points
        assert(len(points[0]) == len(points[-1]) == 3)
        self.data.point.setValue(0, 0, 0)
        self.data.point.setValues(0, len(points), points)

    def set_mouse_over(self):
        if self.enabled:
            self.color.diffuseColor = COLORS[self.ovr_col]

    def unset_mouse_over(self):
        if self.enabled:
            self.color.diffuseColor = COLORS[self.std_col]

    def select(self):
        if self.enabled:
            self.color.diffuseColor = COLORS[self.sel_col]

    def unselect(self):
        if self.enabled:
            self.color.diffuseColor = COLORS[self.std_col]

    def drag(self, mouse_coords, fact=1.):
        if self.enabled:
            pts = self.points
            for i, pt in enumerate(pts):
                pt[0] = mouse_coords[0] * fact + self._tmp_points[i][0]
                pt[1] = mouse_coords[1] * fact + self._tmp_points[i][1]
                pt[2] = mouse_coords[2] * fact + self._tmp_points[i][2]
            self.points = pts
            for foo in self.on_drag:
                foo()

    def drag_release(self):
        if self.enabled:
            for foo in self.on_drag_release:
                foo()

    def drag_start(self):
        self._tmp_points = self.points
        if self.enabled:
            for foo in self.on_drag_start:
                foo()

    @property
    def drag_objects(self):
        if self.enabled:
            return [self]
        return []

    def delete(self):
        if self.enabled and not self._delete:
            self._delete = True

    def check_dependency(self):
        pass


class Marker(Object3D):
    def __init__(self, points, dynamic=False):
        super(Marker, self).__init__(points, dynamic)
        self.marker = coin.SoMarkerSet()
        self.marker.markerIndex = coin.SoMarkerSet.CIRCLE_FILLED_9_9
        self.addChild(self.marker)


class Line(Object3D):
    def __init__(self, points, dynamic=False):
        super(Line, self).__init__(points, dynamic)
        self.drawstyle = coin.SoDrawStyle()
        self.line = coin.SoLineSet()
        self.addChild(self.drawstyle)
        self.addChild(self.line)

class Point(Object3D):
    def __init__(self, points, dynamic=False):
        super(Point, self).__init__(points, dynamic)
        self.drawstyle = coin.SoDrawStyle()
        self.point = coin.SoPointSet()
        self.addChild(self.drawstyle)
        self.addChild(self.point)

class Polygon(Object3D):
    def __init__(self, points, dynamic=False):
        super(Polygon, self).__init__(points, dynamic)
        self.polygon = coin.SoFaceSet()
        self.addChild(self.polygon)

class Arrow(Line):
    def __init__(self, points, dynamic=False, arrow_size=0.04, length=2):
        super(Arrow, self).__init__(points, dynamic)
        self.arrow_sep = coin.SoSeparator()
        self.arrow_rot = coin.SoRotation()
        self.arrow_scale = coin.SoScale()
        self.arrow_translate = coin.SoTranslation()
        self.arrow_scale.scaleFactor.setValue(arrow_size, arrow_size, arrow_size)
        self.cone = coin.SoCone()
        arrow_length = coin.SoScale()
        arrow_length.scaleFactor = (1, length, 1)
        arrow_origin = coin.SoTranslation()
        arrow_origin.translation = (0, -1, 0)
        self.arrow_sep += [self.arrow_translate, self.arrow_rot, self.arrow_scale]
        self.arrow_sep += [arrow_length, arrow_origin, self.cone]
        self += [self.arrow_sep]
        self.set_arrow_direction()

    def set_arrow_direction(self):
        pts = self.points
        self.arrow_translate.translation = tuple(pts[-1])
        direction = pts[-1] - pts[-2]
        direction.normalize()
        _rot = coin.SbRotation()
        _rot.setValue(coin.SbVec3f(0, 1, 0), coin.SbVec3f(*direction))
        self.arrow_rot.rotation.setValue(_rot)

class InteractionSeparator(coin.SoSeparator):
    pick_radius = 10

    def __init__(self, render_manager):
        super(InteractionSeparator, self).__init__()
        self.render_manager = render_manager
        self.objects = coin.SoSeparator()
        self.dynamic_objects = []
        self.static_objects = []
        self.over_object = None
        self.selected_objects = []
        self.drag_objects = []

        self.on_drag = []
        self.on_drag_release = []
        self.on_drag_start = []

        self._direction = None

        self.events = coin.SoEventCallback()
        self += self.events, self.objects

    def register(self):
        self._highlight_cb = self.events.addEventCallback(
            coin.SoLocation2Event.getClassTypeId(), self.highlight_cb)
        self._select_cb = self.events.addEventCallback(
            coin.SoMouseButtonEvent.getClassTypeId(), self.select_cb)
        self._grab_cb = self.events.addEventCallback(
            coin.SoKeyboardEvent.getClassTypeId(), self.grab_cb)
        self._delete_cb = self.events.addEventCallback(
            coin.SoKeyboardEvent.getClassTypeId(), self.delete_cb)
        self._select_all_cb = self.events.addEventCallback(
            coin.SoKeyboardEvent.getClassTypeId(), self.select_all_cb)

    def unregister(self):
        self.events.removeEventCallback(
            coin.SoLocation2Event.getClassTypeId(), self._highlight_cb)
        self.events.removeEventCallback(
            coin.SoMouseButtonEvent.getClassTypeId(), self._select_cb)
        self.events.removeEventCallback(
            coin.SoKeyboardEvent.getClassTypeId(), self._grab_cb)
        self.events.removeEventCallback(
            coin.SoKeyboardEvent.getClassTypeId(), self._delete_cb)
        self.events.removeEventCallback(
            coin.SoKeyboardEvent.getClassTypeId(), self._select_all_cb)
 

    #-----------------------HIGHLIGHTING-----------------------#
    # a SoLocation2Event calling a function which sends rays   #
    # into the scene. This will return the object the mouse is #
    # currently hoovering.                                     #

    def highlight_object(self, obj):
        if self.over_object:
            self.over_object.unset_mouse_over()
        self.over_object = obj
        if self.over_object:
            self.over_object.set_mouse_over()
        self.color_selected()

    def highlight_cb(self, attr, event_callback):
        event = event_callback.getEvent()
        pos = event.getPosition()
        obj = self.send_ray(pos)
        self.highlight_object(obj)

    def send_ray(self, mouse_pos):
        """sends a ray trough the scene and return the nearest entity"""
        ray_pick = coin.SoRayPickAction(self.render_manager.getViewportRegion())
        ray_pick.setPoint(coin.SbVec2s(*mouse_pos))
        ray_pick.setRadius(10)
        ray_pick.setPickAll(True)
        ray_pick.apply(self.render_manager.getSceneGraph())
        picked_point = ray_pick.getPickedPointList()
        return self.obj_by_id(picked_point)

    def obj_by_id(self, picked_point):
        for point in picked_point:
            path = point.getPath()
            length = path.getLength()
            point = path.getNode(length - 2)
            point = list(filter(
                lambda ctrl: ctrl.getNodeId() == point.getNodeId(),
                self.dynamic_objects))
            if point != []:
                return point[0]
        return None
        


#------------------------SELECTION------------------------#
    def select_object(self, obj, multi=False):
        if not multi:
            for o in self.selected_objects:
                o.unselect()
            self.selected_objects = []
        if obj:
            if obj in self.selected_objects:
                self.selected_objects.remove(obj)
            else:
                self.selected_objects.append(obj)
        self.color_selected()
        self.selection_changed()

    def select_cb(self, attr, event_callback):
        event = event_callback.getEvent()
        if (event.getState() == coin.SoMouseButtonEvent.DOWN and
                event.getButton() == event.BUTTON1):
            pos = event.getPosition()
            obj = self.send_ray(pos)
            self.select_object(obj, event.wasCtrlDown())

    def deselect_all(self):
        if self.selected_objects:
            for o in self.selected_objects:
                o.unselect()
            self.selected_objects = []

    def color_selected(self):
        for obj in self.selected_objects:
            obj.select()

    def selection_changed(self):
        pass

    def select_all_cb(self, attr, event_callback):
        event = event_callback.getEvent()
        if (event.getKey() == ord("a")):
            if event.getState() == event.DOWN:
                if self.selected_objects:
                    for o in self.selected_objects:
                        o.unselect()
                    self.selected_objects = []
                else:
                    for obj in self.dynamic_objects:
                        if obj.dynamic:
                            self.selected_objects.append(obj)
                self.color_selected()
                self.selection_changed()


#------------------------INTERACTION------------------------#

    def cursor_pos(self, event):
        pos = event.getPosition()
        return get_point_on_screen(self.render_manager, pos)
    

    def constrained_vector(self, vector):
        if self._direction is None:
            return vector
        if self._direction == "x":
            return [vector[0], 0, 0]
        elif self._direction == "y":
            return [0, vector[1], 0]
        elif self._direction == "z":
            return [0, 0, vector[2]]

    def grab_cb(self, attr, event_callback):
        # press g to move an entity
        event = event_callback.getEvent()
        # get all drag objects, every selected object can add some drag objects
        # but the eventhandler is not allowed to call the drag twice on an object
        if event.getKey() == ord("g"):
            self.drag_objects = set()
            for i in self.selected_objects:
                for j in i.drag_objects:
                    self.drag_objects.add(j)
            # check if something is selected
            if self.drag_objects:
                # first delete the selection_cb, and higlight_cb
                self.unregister()
                # now add a callback that calls the dragfunction of the selected entites
                self.start_pos = self.cursor_pos(event)
                self._dragCB = self.events.addEventCallback(
                    coin.SoEvent.getClassTypeId(), self.dragCB)
                for obj in self.drag_objects:
                    obj.drag_start()
                for foo in self.on_drag_start:
                    foo()


    def dragCB(self, attr, event_callback, force=False):
        event = event_callback.getEvent()
        if ((isinstance(event, coin.SoMouseButtonEvent) and
                event.getState() == coin.SoMouseButtonEvent.DOWN
                and event.getButton() == coin.SoMouseButtonEvent.BUTTON1) or 
                force):
            self.register()
            if self._dragCB:
                self.events.removeEventCallback(
                    coin.SoEvent.getClassTypeId(), self._dragCB)
                self._direction = None
                self._dragCB = None
            self.start_pos = None
            for obj in self.drag_objects:
                obj.drag_release()
            for foo in self.on_drag_release:
                foo()
            self.drag_objects = []
        elif (isinstance(event, coin.SoKeyboardEvent) and
                event.getState() == coin.SoMouseButtonEvent.DOWN):
            if event.getKey() == 65307:     # esc
                for obj in self.drag_objects:
                    obj.drag([0, 0, 0], 1)  # set back to zero
                self.dragCB(attr, event_callback, force=True)
                return
            try:
                key = chr(event.getKey())
            except ValueError:
                # there is no character for this value
                key = "_"
            if key in "xyz" and key != self._direction:
                self._direction = key
            else:
                self._direction = None
            diff = self.cursor_pos(event) - self.start_pos
            diff = self.constrained_vector(diff)
            for obj in self.drag_objects:
                obj.drag(diff, 1)
            for foo in self.on_drag:
                foo()

        elif isinstance(event, coin.SoLocation2Event):
            fact = 0.1 if event.wasShiftDown() else 1.
            diff = self.cursor_pos(event) - self.start_pos
            diff = self.constrained_vector(diff)
            for obj in self.drag_objects:
                obj.drag(diff, fact)
            for foo in self.on_drag:
                foo()

    def delete_cb(self, attr, event_callback):
        event = event_callback.getEvent()
        # get all drag objects, every selected object can add some drag objects
        # but the eventhandler is not allowed to call the drag twice on an object
        if event.getKey() == ord(u"\uffff") and (event.getState() == 1):
            self.remove_selected()

    def remove_selected(self):
        temp = []
        for i in self.selected_objects:
            i.delete()
        for i in self.dynamic_objects + self.static_objects:
            i.check_dependency()    #dependency length max = 1
        for i in self.dynamic_objects + self.static_objects:
            if i._delete:
                temp.append(i)
        self.selected_objects = []
        self.over_object = None
        self.selection_changed()
        for i in temp:
            if i in self.dynamic_objects:
                self.dynamic_objects.remove(i)
            else:
                self.static_objects.remove(i)
            import sys
            self.objects.removeChild(i)
            del(i)
        self.selection_changed()

    # needs upper case as this must overwrite the addChild from coin.SoSeparator
    def removeAllChildren(self, clear_all=False):
        for i in self.dynamic_objects:
            i.delete()
        self.dynamic_objects = []
        self.static_objects = []
        self.selected_objects = []
        self.over_object = None
        if clear_all:
            super(InteractionSeparator, self).removeAllChildren()
        else:
            # only delets graphics objects
            self.objects.removeAllChildren()

    # needs upper case as this must overwrite the addChild from coin.SoSeparator
    def addChild(self, child):
        if hasattr(child, "dynamic"):
            self.objects.addChild(child)
            if child.dynamic:
                self.dynamic_objects.append(child)
            else:
                self.static_objects.append(child)
        else:
            super(InteractionSeparator, self).addChild(child) 
