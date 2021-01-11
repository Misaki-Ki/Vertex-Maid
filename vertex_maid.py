bl_info = {
    "name": "Vertex Maid",
    "author": "Misaki Ki",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Object Properties > Vertex Group Specials", 
    "description": "A collection of tools to help with the maintenance of Vertex Groups",
    "category": "Mesh"
}
import bpy
from bpy.types import Operator


class MESH_OT_Vertex_Group_Cleanup(Operator):
    bl_idname = 'mesh.vertex_group_cleanup'
    bl_label = 'Remove Non-Bone Vertex Groups'
    bl_description = 'Removes Vertex Groups that do not have a matching bone in the selected armature.'
    

    def vertex_group_cleanup_menu(self, context):
        layout = self.layout
        
    @classmethod
    def poll(cls, context):
    # Checking if the first select object is an armature, and that only two objects are selected.
        number_of_selected_objects = len(context.view_layer.objects.selected)
        
        # Checking the amount of selected objects first, that way we don't iterate over a list if it isn't needed.
        if (number_of_selected_objects == 2):
                for objects in context.view_layer.objects.selected:
                    if objects.type == 'ARMATURE':
                        return True
        else: 
            return bpy.context.view_layer.objects.active == 'MESH'
        
    def execute(self, context):
        armature_object = [context.view_layer.objects.selected[i] for i, objects in enumerate(context.view_layer.objects.selected) if objects.type == 'ARMATURE']
        mesh_object = context.view_layer.objects.active
        
        
        # Checking to see if each vertex group is contained in the armature. If it is not, then we'll remove 
        # that vertex group. (N^2)
        for group_index in range(len(mesh_object.vertex_groups) -1, -1, -1):
            if mesh_object.vertex_groups[group_index].name not in armature_object[0].data.bones:
                mesh_object.vertex_groups.remove( mesh_object.vertex_groups[group_index])
        
        

        return {'FINISHED'}
    
    
class MESH_OT_Remove_Empty_Vertex_Groups(Operator):
    bl_idname = 'mesh.remove_empty_vertex_groups'
    bl_label = 'Remove Empty Vertex Groups'
    bl_description = 'Removes Vertex Groups that do not contain any weights'
    
    def execute(self, context):
        mesh_object = context.view_layer.objects.active
        mesh_verticies = mesh_object.data.vertices
        
        # Searching the list in reverse (so python doesn't get jumbled up).
        for vertex_group_index in range(len(mesh_object.vertex_groups) -1, -1, -1):
            if not any(vertex_group_index in [g.group for g in v.groups if g.weight > 0.0] for v in mesh_verticies):
                 mesh_object.vertex_groups.remove(mesh_object.vertex_groups[vertex_group_index])
        return {'FINISHED'}
    
def add_to_menu(self, context):
    self.layout.separator()
    self.layout.operator('mesh.vertex_group_cleanup', icon = 'TRASH')
    self.layout.operator('mesh.remove_empty_vertex_groups')
    
classes = (MESH_OT_Vertex_Group_Cleanup,MESH_OT_Remove_Empty_Vertex_Groups)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.append(add_to_menu)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.remove(add_to_menu)


if __name__ == "__main__":
    register()

