import sys, os, struct

from array import *
from collada import *

polys = []

def writeTo(filename, position, content):
	fh = open(filename, "w+b")
	fh.seek(position)
	fh.write(content)
	fh.close()

def VMAP(verts):
	VMAP = b'VMAP'
	size = 8 + len(verts)*2*2
	VMAP += struct.pack('>I', size)
	for m in range(len(verts)):
		vmap = struct.pack('>H', 0)
		vmap += struct.pack('>H', 0)
		VMAP += vmap
	return VMAP

def INDX(faces):
	INDX = b'INDX'
	size = 8 + len(faces)*2
	INDX += struct.pack('>I', size)
	for l in range(int(len(faces)/3)):
		indx =  struct.pack('>H', int(float(faces[l * 3 + 2])))
		indx += struct.pack('>H', int(float(faces[l * 3 + 1])))
		indx += struct.pack('>H', int(float(faces[l * 3 + 0])))
		INDX += indx
	return INDX

def VERT(verts, normals, uv):
	VERT = b'VERT'
	size = 8 + len(verts)*8*4
	VERT += struct.pack('>I', size)
	for k in range(len(verts)):
		vert =  struct.pack('>f', float(verts[k][0]))
		vert += struct.pack('>f', float(verts[k][1]))
		vert += struct.pack('>f', float(verts[k][2]))
		vert += struct.pack('>f', float(normals[k][0]))
		vert += struct.pack('>f', float(normals[k][1]))
		vert += struct.pack('>f', float(normals[k][2]))
		vert += struct.pack('>f', float(uv[k][0]))
		vert += struct.pack('>f', float(uv[k][1]))
		VERT += vert
	return VERT

def MESH(size, vertSize, vertCount, indxCount):
	MESH = b'MESH'
	MESH += struct.pack('>I', size)
	MESH += struct.pack('>I', 0)
	MESH += struct.pack('>H', vertSize)
	MESH += struct.pack('>H', vertCount)
	MESH += struct.pack('>I', 0)
	MESH += struct.pack('>I', indxCount)
	MESH += struct.pack('>I', 0)
	MESH += struct.pack('>I', 0)
	MESH += struct.pack('>I', 0)
	MESH += struct.pack('>I', 0)
	return MESH

def PADX(size):
	PADX = b'PADX'
	PADX += struct.pack('>I', size)
	for j in range(size-8):
		PADX += b'\xFF'
	return PADX

def build():
	gmx2 = b'GMX2\x00\x00\x00\x08'
	
	content = gmx2
	
	for z in range(len(polys)):
		pad0 = PADX(24)
		mesh = MESH(40, 32, len(polys[z].verts), len(polys[z].faces))
		content += pad0 + mesh
		if(len(polys[z].verts)):
			pad1 = PADX(56)
			vert = VERT(polys[z].verts, polys[z].normals, polys[z].uv0)
			content += pad1 + vert
		if(len(polys[z].faces)):
			pad2 = PADX(24)
			indx = INDX(polys[z].faces)
			vmap = VMAP(polys[z].verts)
			content += pad2 + indx + vmap
	
	endx = b'ENDX\x00\x00\x00\x08'
	
	content += endx
	
	writeTo(sys.argv[1].replace(".dae", ".model"), 0, content)

def main():
	class poly(object):
		def __init__(self):
			self.name = ""
			self.verts = []
			self.normals = []
			self.colors =[]
			self.uv0 = []
			self.uv1 = []
			self.uv2 = []
			self.uv3 = []
			self.faces = []
			self.boneName = []
			self.boneI = []
			self.boneW = []

	global mesh
	
	ii = 0
	
	for i in range(len(mesh.geometries)):
		triset = mesh.geometries[i].primitives[0]
		
		vertex = triset.vertex.tolist()
		normal = triset.normal
		texcoordset = triset.texcoordset[0].tolist()
		indices = list(triset.vertex_index)
		
		Normals = []
		for k in range(len(vertex)):
			nrm = [0.0, 0.0, 0.0]
			iii = 0
			usedNRMs = []
			for vertIdx in indices:
				if(vertIdx == k and triset.normal_index[iii] not in usedNRMs):
					nrm += normal[triset.normal_index[iii]]
					usedNRMs.append(triset.normal_index[iii])
				iii += 1
			Normals.append(list(nrm))
		
		uniqueVerts = []
		correctIndices = []
		for i in range(len(indices)):
			vert = [vertex[indices[i]], Normals[indices[i]], texcoordset[triset.texcoord_indexset[0][i]]]
			if(vert not in uniqueVerts):
				uniqueVerts.append(vert)
				if(i not in correctIndices):
					try:
						correctIndices.append(max(correctIndices) + 1)
					except:
						correctIndices.append(0)
				else:
					correctIndices.append(indices[i])
			else:
				#	'X' is inserted so the lengths of uniqueVerts and correctIndices stay the same
				uniqueVerts.append('X')
				correctIndices.append(correctIndices[uniqueVerts.index(vert)])
		
		correctVerts = []
		correctNormals = []
		correctTexCoords = []
		
		for j in range(len(uniqueVerts)):
			#	Here 'X' is filtered out again, as it is no longer needed for differentiation
			if(uniqueVerts[j] is not 'X'):
				correctVerts.append(uniqueVerts[j][0])
				correctNormals.append(uniqueVerts[j][1])
				correctTexCoords.append(uniqueVerts[j][2])
		
		#print(correctVerts)
		#print(correctNormals)
		#print(correctTexCoords)
		#print(correctIndices)
		
		'''
		correctVerts = []
		for vertIdx in triset.vertex_index:
			correctVerts.append(vertex[vertIdx])
		
		correctNormals = []
		Normals = []
		for k in range(len(list(vertex))):
			nrm = [0.0, 0.0, 0.0]
			iii = 0
			usedNRMs = []
			for vertIdx in triset.vertex_index:
				if(vertIdx == k and triset.normal_index[iii] not in usedNRMs):
					nrm += normal[triset.normal_index[iii]]
					usedNRMs.append(triset.normal_index[iii])
				iii += 1
			Normals.append(list(nrm))
		for vertIdx in triset.vertex_index:
			correctNormals.append(Normals[vertIdx])
		
		correctTexCoords = []
		for texCoordIdx in triset.texcoord_indexset[0]:
			correctTexCoords.append(texcoordset[texCoordIdx])
		
		correctIndices = []
		for index in range(int(len(indices)/3)):
			correctIndices.append([indices[index * 3], indices[index * 3 + 1], indices[index * 3 + 2]])
		'''
		
		if(ii > 0):
			polys.append(data)
		data = poly()
		ii += 1
		
		#print(triset.vertex_index)
		#print(triset.normal_index)
		#print(triset.texcoord_indexset[0])
		
		data.verts = correctVerts
		data.normals = correctNormals
		data.uv0 = correctTexCoords
		data.faces = correctIndices
	
	polys.append(data)
	
	#print("Verts: ")
	#print(polys[0].verts)
	#print("Normals: ")
	#print(polys[0].normals)
	#print("UVs: ")
	#print(polys[0].uv0)
	#print("Indices: ")
	#print(polys[0].faces)
	
	build()


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('Insufficient arguments. Please supply one DAE model.')
		exit()
	else:
		global mesh
		#f = open(sys.argv[1])
		mesh = Collada(sys.argv[1])
		main()
		print("I would think it worked.")
