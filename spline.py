from typing import List, Tuple

#original author - Ian Mallett
#graciously allowed the use of this code ( - Kochanek-Bartels Spline - 1.0.0 - May 2008) under the GPL

class Spline():

	def __init__(self):
		self.c = 0
		self.b = 0
		self.t = 0
		self.ControlPoints = []
		self.subpoints = []
		
	def nearestPoint(self, pos):
		shortest = 999999
		nearest = None
		ControlPoints = self.ControlPoints
		for cp in ControlPoints:
			xd = cp[0]-pos[0]
			yd = cp[1]-pos[1]
			td = xd*xd+yd*yd
			if td<shortest:
				shortest = td
				nearest = cp
		return nearest, shortest
	
	def nearestSubPoint(self, pos):
		shortest = 999999
		nearest = None
		ControlPoints = self.subpoints
		for cp in ControlPoints:
			xd = cp[0]-pos[0]
			yd = cp[1]-pos[1]
			td = xd*xd+yd*yd
			if td<shortest:
				shortest = td
				nearest = cp
		return nearest, shortest

	def DrawCurve(self):
		# calculate points
		closed_loop = True
		subpoints = Spline.interpolate_kochanek_bartel(self.ControlPoints, self.t, self.c, self.b, closed_loop)

		# round float values to int for screen pixel values
		self.subpoints = [(int(round(x)), int(round(y))) for (x, y) in subpoints]
		return self.subpoints

	@staticmethod
	def _calc_tangents(control_points: List[Tuple[float, float]], t: float, c: float, b: float)\
		-> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:

		tans = []
		tand = []

		cona = (1 - t) * (1 + b) * (1 - c) * 0.5
		conb = (1 - t) * (1 - b) * (1 + c) * 0.5
		conc = (1 - t) * (1 + b) * (1 + c) * 0.5
		cond = (1 - t) * (1 - b) * (1 - c) * 0.5

		for i in range(1, len(control_points) - 1):
			pa = control_points[i - 1]
			pb = control_points[i]
			pc = control_points[i + 1]

			x1 = pb[0] - pa[0]
			y1 = pb[1] - pa[1]
			# z1 = pb[2] - pa[2]
			x2 = pc[0] - pb[0]
			y2 = pc[1] - pb[1]
			# z2 = pc[2] - pb[2]

			tans.append((cona * x1 + conb * x2, cona * y1 + conb * y2))  # cona*z1+conb*z2
			tand.append((conc * x1 + cond * x2, conc * y1 + cond * y2))  # conc*z1+cond*z2

		return tans, tand

	@staticmethod
	def interpolate_kochanek_bartel(
			control_points: List[Tuple[float, float]], t: float, c: float, b: float, t_inc: float = 0.2, closed: bool = True)\
		-> List[Tuple[float, float]]:
		"""
		Interpolates Kochanek-Bartels spline.
		:param control_points:
		:param t: tension
		:param c: continuity
		:param b: bias
		:param t_inc: max length between interpolated points
		:param closed: closed circle or line
		:return:
		"""

		if closed:
			control_points = [control_points[-1]] + control_points + [control_points[0]]
		else:
			control_points = [control_points[0]] + control_points + [control_points[-1]]

		tans, tand = Spline._calc_tangents(control_points, t, c, b)

		if closed:
			control_points.append(control_points[2])
			tans.append(tans[0])
			tand.append(tand[0])

		final_lines = []
		for i in range(1, len(control_points) - 2):
			print("i", i)

			p0 = control_points[i]
			p1 = control_points[i + 1]
			m0 = tand[i-1]
			m1 = tans[i]

			# interpolate curve from p0 to p1
			final_lines.append((p0[0], p0[1]))
			t_iter = t_inc
			while t_iter < 1.0:
				t_iter_2 = t_iter ** 2
				t_iter_3 = t_iter ** 3

				h00 = 2*t_iter_3 - 3*t_iter_2 + 1
				h10 = 1*t_iter_3 - 2*t_iter_2 + t_iter
				h01 = -2*t_iter_3 + 3*t_iter_2
				h11 = 1*t_iter_3 - 1*t_iter_2

				px = h00*p0[0] + h10*m0[0] + h01*p1[0] + h11*m1[0]
				py = h00*p0[1] + h10*m0[1] + h01*p1[1] + h11*m1[1]
				#pz = h00*p0[2] + h10*m0[2] + h01*p1[2] + h11*m1[2]

				final_lines.append((px, py))
				t_iter += t_inc

			final_lines.append((p1[0], p1[1]))

		return final_lines

	@staticmethod
	def interpolate_catmull_rom(control_points: List[Tuple[float, float]], t_inc: float = 0.2)\
		-> List[Tuple[float, float]]:
		return Spline.interpolate_kochanek_bartel(control_points, 0, 0, 0, t_inc)
