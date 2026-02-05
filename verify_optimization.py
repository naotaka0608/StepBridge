
import sys
from pathlib import Path

# Add src to python path
root_dir = Path(__file__).parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopLoc import TopLoc_Location
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorGen
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB

from step_to_obj.converter import extract_all_meshes

def create_test_doc_with_sphere():
    # Create valid OCP document
    doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF"))
    shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    
    # Make a sphere (radius 10)
    # Sphere has smooth normals, so vertices should be shared
    sphere = BRepPrimAPI_MakeSphere(10.0).Shape()
    
    # Add to doc
    label = shape_tool.AddShape(sphere)
    
    # Set Color (Red)
    color = Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB)
    color_tool.SetColor(label, color, XCAFDoc_ColorGen)

    return doc, shape_tool, color_tool

def test_optimization():
    print("Initializing test environment...")
    doc, shape_tool, color_tool = create_test_doc_with_sphere()
    
    print("Extracting meshes (with optimization)...")
    # Deflection 0.1 for decent quality
    parts = extract_all_meshes(doc, shape_tool, color_tool, linear_deflection=0.1, angular_deflection=0.5)
    
    vertex_count = sum(len(p.vertices) for p in parts)
    face_count = sum(len(p.faces) for p in parts)
    
    print(f"Result: {vertex_count} vertices, {face_count} triangles")
    
    # Theoretical Check
    # A triangulated sphere with shared vertices has roughly V ~= T/2 + 2
    # Without optimization (separate faces), V = 3 * T
    
    ratio = vertex_count / face_count
    print(f"Vertex/Face Ratio: {ratio:.2f}")
    
    if ratio < 1.0:
        print("SUCCESS: Vertices are being shared (Ratio < 1.0)")
        print("Optimization is WORKING.")
    else:
        print("FAILURE: Vertices are NOT being shared (Ratio >= 1.0 is likely unoptimized)")
        print(f"Expected Ratio ~0.5, Got {ratio:.2f}")

if __name__ == "__main__":
    test_optimization()
