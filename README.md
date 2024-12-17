![RCAIDE_Logo](link)

 #

<div align="center">
 
[![readthedocs](https://readthedocs.org/projects/pybamm/badge/?version=latest)](https://docs.pybamm.org/en/latest/?badge=latest) 
[![DOI](https://zenodo.org/badge/DOI/10.5334/jors.309.svg)](https://doi.org/10.5334/jors.309) 

</div>



[RCAIDE: Research Community Aircraft Interdisciplinary Design Environment]([link](https://www.rcaide.leadsresearchgroup.com/))
=======

The Research Community Aircraft Interdisciplinary Design Environment, or RCAIDE  (pronounced “arcade”) is a powerful open-source Python platform that revolutionizes aircraft design and analysis. From commercial airliners to UAVs and next-generation hybrid-electric aircraft, RCAIDE provides comprehensive multi-disciplinary analysis tools backed by validated engineering methods. Our streamlined workflow and modular architecture help aerospace engineers and researchers accelerate development cycles and explore innovative designs with confidence. RCAIDE-LEADS is a form from RCAIDE, developed and maintained by the [Lab for Electric Aircraft Design and Sustainability](https://www.leadsresearchgroup.com/)
 
## Transinitign from SUAVE Legacy 
RCAIDE was built to allow users to transition their work to smoothly from SUAVE to RCAIDE. The organization of RCAIDE’s code structure was done such that a SUAVE user can understand it, but breaks free of some of the antiquated nomenclature. To maintain backwards compatibility for the first release, a frozen version of SUAVE is packaged as a library. This enables users to access the deprecated SUAVE features as RCAIDE’s abilities grow.
 
## Code Architecture 
The code is arranged into repositories that house native data structures, functions, components, and subroutines for discipline analyses and support number-crunching operations. This allows for intuitive navigation by developers or avid users seeking to modify the source code. Solely written in Python, an RCAIDE installation
appears in one repository that is itself organized into two secondary-level repositories: 
* **RCAIDE** sub-directory, where their source code resides
* **Regressions** sub-directory, where unit tests for verification and validation are performed.

```mermaid
%%{init: {'flowchart': {'curve': 'linear', 'nodeSpacing': 50, 'rankSpacing': 50}}}%%
flowchart LR
    RCAIDE_LEADS[RCAIDE_LEADS]
    RCADIE[RCADIE]
    Regressions[Regressions]
    
    RCAIDE_LEADS ---> RCADIE
    RCAIDE_LEADS ---> Regressions

    style RCAIDE_LEADS fill:#0d6dc5,color:#fff
    style RCADIE fill:#09d0d9,color:#fff
    style Regressions fill:#09d0d9,color:#fff
```
The RCAIDE subdirectory is arranged into frameworks and methods modules. Its predecessor, SUAVE, was written primarily as a superseding framework. Think of framework modules as the glue or roadmap that connects all the functions housed in the Library folder. The framework folder mainly comprises core data structures, classes instances of the various methods within the code, the mission and energy networks and the optimization framework. The Library module comprises five tertiary submodules: Attributes, Components,  Methods, Mission and Plots.

```mermaid
%%{init: {'flowchart': {'curve': 'linear', 'nodeSpacing': 50, 'rankSpacing': 50}}}%%
flowchart LR
    RCADIE[RCADIE]
    Framework[Framework]
    Libraries[Libraries]
    
    RCADIE ---> Framework
    RCADIE ---> Libraries

    style RCADIE fill:#09d0d9,color:#fff
    style Framework fill:#0fcf99,color:#fff
    style Libraries fill:#0fcf99,color:#fff
```
## Capabilities of RCAIDE
RCAIDE currently possesses the ability to perform the following analyses, each at varying levels of fidelity. Here, we define fidelity as a level of accuracy to the actual physical value. As the level of fidelity increases, so does accuracy. However, this comes with the penalty of computational time and memory.  Having multi-fidelity capability allows RCAIDE to perform energy network analysis, complete flight  vehicle mission analysis, multi-fidelity optimization, design space exploration, artificial intelligence, and model-based systems engineering. Here are some notable use cases of RCAIDE: 
 (link to tutorials)

* Mission Analysis   
* Optimization 
    * Gradient-based optimization
    * Non-gradient-based optimization
    * Multi-fidelity optimization
* Performance Analysis
    * Payload range 
    * Aerodynamic analysis
    * V-N diagrams
    * Propeller analysis 
    * Takeoff Field Length Estimation
* Weights Analysis
    * Operating Empty Weight, Zero Fuel Weight estimation
    * Component weight estimation 
    * Center of Gravity estimation
    * Moment of Intertia estimation 

  

## Installing RCAIDE 

RCAIDE is available on GNU/Linux, MacOS and Windows. We strongly recommend installing RCAIDE within a Python virtual environment to avoid altering any distribution of Python files. Please review the documentation for instructions on creating a virtual environment for RCAIDE.

Requirements
------------

numpy, scipy, matplotlib, pip, scikit-learn, plotly


Simple Setup
------------

```
git clone https://github.com/suavecode/SUAVE.git
cd SUAVE/trunk
python setup.py install
``` 

Developer Install 
-----------------
* See [develop](http://suave.stanford.edu/download/develop_install.html).


* Using pip (coming soon) 
* Using conda (coming soon) 


## 📑 Citing RCAIDE
While we do not have 

## 🛠️ Contributing to RCAIDE
Contributing Institutions
-------------------------
* Aerospace Research Community, LLC
* University of Illinois Lab for Electric Aircraft Design and Sustainability ([leadsresearchgroup.com](https://www.leadsresearchgroup.com/)) 
* Stanford University Aerospace Design Lab ([adl.stanford.edu](http://adl.stanford.edu))
  
Contributing Developers
----------------------- 
* Emilio Botero 
* Jordan Smart 
* Matthew Clarke 
* Racheal Erhard
* Lab for Electric Aircraft Design and Sustainability ([leadsresearchgroup.com]

Getting Involved 
----------------------- 

If you'd like to help us develop RCAIDE by adding new methods, writing documentation, or fixing embarrassing bugs, please look at these [guidelines](link) first.
Submit improvements or new features with a [pull request] (link)

## 📫 Get in touch

Share feedback, report issues, and request features via or [Github Issues](link)
Engage with peers and maintainers in [Discussions] (link)

For any questions, comments, suggestions or bug reports, please see the
[contact page](link).

## 📃 License

RCAIDE-LEADS  is fully open-source. For more information about its license, see [LICENSE](link).


