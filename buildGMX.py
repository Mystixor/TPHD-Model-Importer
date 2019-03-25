import sys, os, struct

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
	size = 8 + len(faces)*3*2
	INDX += struct.pack('>I', size)
	for l in range(len(faces)):
		indx =  struct.pack('>H', int(float(faces[l][2])) - 1)
		indx += struct.pack('>H', int(float(faces[l][1])) - 1)
		indx += struct.pack('>H', int(float(faces[l][0])) - 1)
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
	MESH += struct.pack('>I', indxCount * 3)
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
	pad0 = PADX(24)
	mesh = MESH(40, 32, len(polys[0].verts), len(polys[0].faces))
	pad1 = PADX(56)
	vert = VERT(polys[0].verts, polys[0].normals, polys[0].uv0)
	pad2 = PADX(24)
	indx = INDX(polys[0].faces)
	vmap = VMAP(polys[0].verts)
	endx = b'ENDX\x00\x00\x00\x08'
	
	content = gmx2 + pad0 + mesh + pad1 + vert + pad2 + indx + vmap + endx
	
	writeTo(sys.argv[1].replace(".csv", ".gmx"), 0, content)

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

	curPoly = 0
	
	ii = 0
	for line in f:
		if line.startswith("Obj Name"):
			if(ii > 0):
				polys.append(data)
			data = poly()
			data.name = line.split(":")[1].replace("\n", "")
			ii += 1
			SubType = 0
		elif line.startswith("tex_Array:"):
			pass
		elif line.startswith("Bone_Suport"):
			pass
		elif line.startswith("Color_Suport"):
			colorEnable = True
		elif line.startswith("UV_Num:"):
			numUVs = int(line.split(":")[1].replace("\n", ""))
		elif line.startswith("vert_Array"):
			Type = 1
		elif line.startswith("face_Array"):
			Type = 2
		elif line.startswith("bone_Array"):
			Type = 3
		else:
			line = line.replace("\n", "").replace("\r", "").split(",")
			if(Type == 1):
				if(SubType == 0):
					data.verts.append(line)
					SubType += 1
				elif(SubType == 1):
					data.normals.append(line)
					SubType += 1
				elif(SubType == 2):
					data.colors.append(line)
					SubType += 1
				elif(SubType == 3):
					data.uv0.append(line)
					if(numUVs == 1):SubType = 0
					else:SubType += 1
				elif(SubType == 4):
					data.uv1.append(line)
					if(numUVs == 2):SubType = 0
					else:SubType += 1
				elif(SubType == 5):
					data.uv2.append(line)
					if(numUVs == 3):SubType = 0
					else:SubType += 1
				elif(SubType == 6):
					data.uv3.append(line)
					SubType = 0
			elif(Type == 2):
				data.faces.append(line)
			elif(Type == 3):
				line.pop()
				bbs = 0
				StrNames = []
				BonArry = []
				for obj in line:
						
						if(bbs == 0):
								StrNames.append(obj)
								bbs += 1
						else:
								BonArry.append(float(obj))
								bbs = 0
				data.boneName.append(StrNames)
				data.boneW.append(BonArry)
				
	polys.append(data)

	build()


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('Insufficient arguments. Please supply one CSV model.')
		exit()
	else:
		f = open(sys.argv[1])
		main()
		print("I would think it worked.")