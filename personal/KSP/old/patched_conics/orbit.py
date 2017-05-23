
""" describe an orbit
p - plane
a - semi major axis
e - eccentricity

"""
class Orbit:
	def __init__(self, p, a, e):
		self.p = p
		self.a = a
		self.e = e

class Ellipse(Orbit):
	

class Parabola(Orbit):


class Hyperbola(Orbit):




"""
determine type of orbit and orbital characteristics
"""
def compute(b1, b2, x1, v1, time):

	#cout << "compute orbit of " << b1->name_ << " around " << b2->name_ << endl;

	v = v1 - b2.v(time);
	r = x1 - b2.x(time);
	
	x2 = b2.x(time);
	
	#cout << "b1->x"
	#	<< setw(16) << x1[0]
	#	<< setw(16) << x1[1]
	#	<< setw(16) << x1[2]
	#	<< endl;
	#cout << "b2->x"
	#	<< setw(16) << x2[0]
	#	<< setw(16) << x2[1]
	#	<< setw(16) << x2[2]
	#	<< endl;

	
	h = glm::cross(r, v);
	
	
	mu = 6.67E-11 * (b1->m_ + b2->m_);
	
	specific_orbital_energy = pow(glm::length(v), 2.0) / 2.0 - mu / glm::length(r);
	
	a = -mu / 2.0 / specific_orbital_energy;
	
	float tmp = 2.0 * specific_orbital_energy * pow(glm::length(h), 2.0) / pow(mu, 2.0);
	float e = sqrt(1.0 + tmp);

	/*
	   cout << "tmp " << tmp << endl;
	   cout << "r   " << glm::length(r) << endl;
	   cout
	   << setw(16) << r[0]
	   << setw(16) << r[1]
	   << setw(16) << r[2]
	   << endl;
	   */

	# eccentricity vector
	E = np.cross(v, h) / mu - r / np.length(r);
	
	true_anomaly = acos(glm::dot(E, r) / glm::length(E) / glm::length(r));
	
	if(np.dot(r, v) < 0.0):
		true_anomaly = TAU - true_anomaly;
	
	# orbital plane x
	x = glm::rotate(r, -true_anomaly, h);
	x = glm::normalize(x);
	
	plane pl(glm::normalize(h), b2->x(time), x);
	
	conic* o = 0;

	cout << "v " << glm::length(v) << endl;
	cout << "r " << glm::length(r) << endl;
	cout << "e " << e << endl;

	if(e >= 0.0 && e < 1.0) {
		o = new ellipse(pl, a, sqrt(pow(a, 2) * (1.0 - pow(e, 2))), e);
	} else if(e == 1.0) {
		//o = new parabola(pl, a, e);
	} else if(e > 1.0) {
		//float b = sqrt(pow(a, 2) * (pow(e, 2) - 1.0));
		//o = new hyperbola(pl, a, b, e);
	} else {
		abort();
	}

	assert(o);

	o->b1_ = b1;
	o->b2_ = b2;
	o->h_ = h;
	o->mu_ = mu;
	o->specific_orbital_energy_ = specific_orbital_energy;

	return o;








struct conic: orbit {
	conic(plane p, float a, float e): plane_(p), a_(a), e_(e) {}

	static conic*		compute(body* b1, body* b2, glm::vec3 x, glm::vec3 v, float time);

	virtual float		x(float) = 0;
	virtual float		y(float) = 0;


	float			mu_;
	float			specific_orbital_energy_;
	glm::vec3		h_;

	float			epoch_;

	body*			b1_;
	body*			b2_;

	state*			state_escape;
	state*			state_encounter;
	orbit*			next_;



	// geometry
	plane			plane_;
	float			a_;
	float			e_; // eccentricity
	float			p_;


	// equations of motion
	virtual float		mean_anomaly_from_time_from_periapsis(float time) = 0;
	virtual float		period() = 0;
	virtual float		eccentric_anomaly_from_mean_anomaly(float M) = 0;
	virtual float		mean_anomaly_from_eccentric_anomaly(float E) = 0;


	void			generate_line(float a, float b) {
		float t = a;
		int n = 100;
		float dt = (b - a) / (float)n; //2.0 * M_PI / (float)n;

		line_.clear();

		for(int i = 0; i < n; i++) {

			glm::vec3 point = x(t) * plane_.x_ + y(t) * plane_.y_;

			line_.push_back(point);

			//cout << setw(8) << point[0] << setw(8) << point[1] << setw(8) << point[2] << endl;

			t += dt;
		}
	}

	virtual void		standard_line() = 0;


	vector<glm::vec3>	line_;
};

struct parabola: conic {
	parabola(plane p, float a, float e):
		conic(p, a, e)
	{
	}
	virtual void		standard_line() {
		generate_line(-1,1);
	}
	virtual void		draw() {
		glColor3fv(colorWhite);
		abort();
		line_strip(line_);
	}
	float		x(float t) {
		return a_ * t * t - a_;
	}
	float		y(float t) {
		return 2.0 * a_ * t;
	}
};
struct hyperbola: conic {
	hyperbola(plane p, float a, float b, float e):
		conic(p, a, e),
		b_(b)
	{
	}
	virtual void		standard_line() {
		generate_line(-1,1);
	}
	float		x(float t) {
		return a_ / cos(t);
	}
	float		y(float t) {
		return b_ * tan(t);
	}
	virtual void	draw() {
		glColor3fv(colorWhite);
		abort();
		line_strip(line_);
	}
	float		b_;
};