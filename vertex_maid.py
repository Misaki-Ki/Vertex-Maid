bl_info = {
    "name": "Vertex Maid",
    "author": "Misaki Ki",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Object Properties > Vertex Group Specials", 
    "description": "A collection of tools to help with the maintenance of Vertex Groups"
}
import bpy


class MESH_OT_Vertex_Group_Cleanup(bpy.types.Operator):
    bl_idname = 'mesh.vertex_group_cleanup'
    bl_label = 'Remove Non-Bone Vertex Groups'
    bl_description = 'Removes Vertex Groups that do not have a matching bone in the selected armature.'
    

    def vertex_group_cleanup_menu(self, context):
        layout = self.layout
        
    @classmethod
    def poll(cls, context):
    
        first_object = context.view_layer.objects.selected[1]
        second_object = context.view_layer.objects.selected[0]
        
        
        # Checking if the first select object is an armature, and that only two objects are selected.
        return first_object.type == 'ARMATURE' and (len(context.view_layer.objects.selected) == 2)
        
    def execute(self, context):    
        armature_object = context.view_layer.objects.selected[1]
        mesh_object = context.view_layer.objects.selected[0]
        
        
        # Checking to see if each vertex group is contained in the armature. If it is not, then we'll remove 
        # that vertex group. (N^2)
        for group in mesh_object.vertex_groups[:]:
            if group.name not in armature_object.data.bones:
                mesh_object.vertex_groups.remove(group)
        
        

        return {'FINISHED'}
    
    print('Vertex Group Cleanup Successfully Added.')
    

def add_to_menu(self, context):
    self.layout.separator()
    self.layout.operator('mesh.vertex_group_cleanup', icon = 'TRASH')
    
classes = (MESH_OT_Vertex_Group_Cleanup,)

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

