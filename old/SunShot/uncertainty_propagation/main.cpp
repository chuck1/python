#include <iostream>
#include <cmath>

struct umode {
	enum e {
		ABS,
		REL
	};
};

template<typename T> struct value
{
	public:
		typedef value<T> V;

		value(T nv, T nu, umode::e nmode): v(nv), u(nu), mode(nmode) {}

		value<T>	operator*(value<T> t)
		{
			return value<T>(v * t.v, ur() + t.ur(), umode::REL);
		}
		value<T>	operator/(value<T> t)
		{
			return value<T>(v / t.v, ur() + t.ur(), umode::REL);
		}


		value<T>	operator*(T t)
		{
			return value<T>(v * t, u, mode);
		}

		value<T>	operator+(value<T> t)
		{
			return value<T>(v + t.v, ua() + t.ua(), umode::ABS);
		}
		value<T>	operator-(value<T> t)
		{
			return value<T>(v - t.v, ua() + t.ua(), umode::ABS);
		}

		value<T>	pow(T t)
		{
			return value<T>(::pow(v,t), ur() * t, umode::REL);
		}

		T		ua()
		{
			if(mode == umode::ABS) return u;
			else return u*v;
		}
		T		ur()
		{
			if(mode == umode::REL) return u;
			else return u/v;
		}
		T		get_v() const { return v; }
	private:
		T		v;
		T		u;

		umode::e	mode;	
};

typedef value<float> vfloat;

vfloat radiation_loss(vfloat T, vfloat T_inf, vfloat emiss)
{
	return  emiss * (T.pow(4) - T_inf.pow(4)) * 5.67E-8;
}
vfloat convection_loss(vfloat T, vfloat T_inf, vfloat hnat)
{
	return  hnat * (T - T_inf);
}

value<float> efficiency_thermal_sim()
{
	vfloat T(989.70, 0.0, umode::REL);
	vfloat T_inf_r(298.15, 0.0, umode::REL);
	vfloat T_inf_c(298.15, 0.0, umode::REL);
	vfloat emiss(0.75, 0.0, umode::REL);
	vfloat hnat(15,0.0, umode::REL);

	vfloat q(6.9E5, 0.1, umode::REL);

	vfloat q_loss_r = radiation_loss(T, T_inf_r, emiss);

	vfloat q_loss_c = convection_loss(T, T_inf_c, hnat);

	value<float> te = q / (q + q_loss_r + q_loss_c);

	return te;
}

vfloat efficiency_thermal_exp()
{


	

}

int main()
{




	value<float> te_sim = efficiency_thermal_sim();


	std::cout << "thermal eff sim = " << te_sim.get_v() << " +/- " << te_sim.ua() << std::endl;







}

