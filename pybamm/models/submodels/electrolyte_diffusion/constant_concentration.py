#
# Class for leading-order electrolyte diffusion employing stefan-maxwell
#
import pybamm

from .base_electrolyte_diffusion import BaseElectrolyteDiffusion


class ConstantConcentration(BaseElectrolyteDiffusion):
    """Class for constant concentration of electrolyte

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel
    options : dict, optional
        A dictionary of options to be passed to the model.

    **Extends:** :class:`pybamm.electrolyte_diffusion.BaseElectrolyteDiffusion`
    """

    def __init__(self, param, options=None):
        super().__init__(param, options)

    def get_fundamental_variables(self):
        c_e_dict = {
            domain: pybamm.FullBroadcast(1, domain.lower(), "current collector")
            for domain in self.domains
        }
        variables = self._get_standard_concentration_variables(c_e_dict)

        N_e = pybamm.FullBroadcastToEdges(
            0, [domain.lower() for domain in self.domains], "current collector"
        )

        variables.update(self._get_standard_flux_variables(N_e))

        return variables

    def get_coupled_variables(self, variables):
        eps_c_e = {}
        for domain in self.domains:
            eps_k = variables[f"{domain} porosity"]
            c_e_k = variables[f"{domain.split()[0]} electrolyte concentration"]
            eps_c_e[domain] = eps_k * c_e_k
        variables.update(
            self._get_standard_porosity_times_concentration_variables(eps_c_e)
        )

        return variables

    def set_boundary_conditions(self, variables):
        """
        We provide boundary conditions even though the concentration is constant
        so that the gradient of the concentration has the correct shape after
        discretisation.
        """

        c_e = variables["Electrolyte concentration"]

        self.boundary_conditions = {
            c_e: {
                "left": (pybamm.Scalar(0), "Neumann"),
                "right": (pybamm.Scalar(0), "Neumann"),
            }
        }

    def set_events(self, variables):
        # No event since the concentration is constant
        pass
