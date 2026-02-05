
import sys
from pathlib import Path

# Add src to python path
root_dir = Path(__file__).parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

from step_to_obj.converter import MeshPart, write_fbx_file

def test_fbx_writer():
    output_path = Path("test_output_box.fbx")
    
    # Create a simple Cube manually (6 faces, 4 vertices each)
    # Positions
    p000 = (0,0,0)
    p100 = (1,0,0)
    p110 = (1,1,0)
    p010 = (0,1,0)
    p001 = (0,0,1)
    p101 = (1,0,1)
    p111 = (1,1,1)
    p011 = (0,1,1)
    
    # Simple single face (Bottom) z=0: 000, 100, 110, 010
    # Normal (0,0,-1) at all corners
    b_verts = [p000, p100, p110, p010] 
    b_norms = [(0,0,-1), (0,0,-1), (0,0,-1), (0,0,-1)]
    b_faces = [(0,1,2), (0,2,3)] # 2 triangles
    
    # Top face z=1: 001, 101, 111, 011
    # Normal (0,0,1)
    t_verts = [p001, p101, p111, p011]
    t_norms = [(0,0,1), (0,0,1), (0,0,1), (0,0,1)]
    t_faces = [(4,5,6), (4,6,7)] # Indices relative to start of vertices list in MeshPart?
    # MeshPart has flat list of vertices.
    
    # Combine into one MeshPart
    # Vertices: 4 bottom + 4 top = 8 vertices? 
    # Wait, my extraction logic produced unique vertices for sharp edges.
    # So extraction would produce 4 verts for Bottom, 4 for Top. Total 8.
    
    vertices = b_verts + t_verts
    normals = b_norms + t_norms
    
    # Faces: triangles.
    # Bottom: 0,1,2 and 0,2,3
    # Top: 4,5,6 and 4,6,7
    faces = [(0,1,2), (0,2,3), (4,5,6), (4,6,7)]
    
    part = MeshPart(
        name="TestBox",
        vertices=vertices,
        faces=faces,
        normals=normals,
        color=(1,0,0)
    )
    
    print(f"Input: {len(vertices)} vertices, {len(normals)} normals")
    
    write_fbx_file(output_path, [part])
    
    print(f"Written to {output_path}")
    
    # Inspect File Content
    content = output_path.read_text(encoding="utf-8")
    
    # Check for IndexToDirect
    if 'ReferenceInformationType: "IndexToDirect"' in content:
        print("SUCCESS: Found IndexToDirect for Normals")
    else:
        print("FAILURE: Did not find IndexToDirect")
        
    # Check Vertices array length
    # Should be 8 vertices * 3 = 24 floats
    # "Vertices: *24 {"
    if "Vertices: *24 {" in content:
        print("SUCCESS: Vertices count is 8 (minimal).")
    else:
        print("FAILURE: Vertices count is NOT 8.")
        
    # Check Normals array length
    # Should be 2 unique normals * 3 = 6 floats
    # "Normals: *6 {"
    if "Normals: *6 {" in content:
        print("SUCCESS: Unique Normals count is 2.")
    else:
        print("FAILURE: Unique Normals count is NOT 2.")
        
    # Check NormalsIndex
    if "NormalsIndex: *" in content:
        print("SUCCESS: Found NormalsIndex array.")
    else:
         print("FAILURE: NormalsIndex missing.")

if __name__ == "__main__":
    test_fbx_writer()
