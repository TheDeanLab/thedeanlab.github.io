Data Management
===============

This page covers how the lab stores research data and how microscopy images
should be prepared for internal and external presentation.

Data Storage
------------

- All lab data should be stored on `BioHPC <https://portal.biohpc.swmed.edu/content/>`_.
- New users should register for an account at
  `BioHPC account registration <https://portal.biohpc.swmed.edu/accounts/register/>`_.
- BioHPC access is a standard requirement for working in the lab, and new users
  are typically directed to an orientation or training session during setup.
  See :doc:`cloud-usage` if this information has not yet been provided.
- The primary archive location for lab data is ``/archive``.
- Organize data routinely and remove material that no longer needs to be kept;
  storage has a real operational cost.
- If data support a manuscript, preserve the raw data in a recoverable form.
- If compression is used for archived data, it should be lossless.

Best Practices for Digital Images
---------------------------------

Microscopy data are quantitative, and image display choices can either clarify
or distort that information. Use the following practices when preparing figures,
slides, or internal review materials.

Scale bars
^^^^^^^^^^

- Include a clearly labeled scale bar on microscopy images.
- In Fiji, confirm the pixel size with ``Analyze > Set Scale`` before adding the
  scale bar.
- Add a scale bar with ``Analyze > Tools > Scale Bar``.
- Flatten overlays before export if the image will be viewed outside Fiji or
  ImageJ.
- Sanity-check the displayed scale against a known biological feature.

Gamma
^^^^^

- Any gamma correction should be disclosed in a manuscript, slide deck, or other
  context where the image is presented as data.
- Gamma correction is non-linear and can make an image unsuitable for
  quantitative interpretation.
- Perform measurements on raw image data, not on gamma-adjusted exports.

Lookup tables
^^^^^^^^^^^^^

- For single-channel data, grayscale is usually the clearest choice.
- For multichannel data, prefer color combinations that remain interpretable to
  colorblind viewers, such as green/magenta instead of red/green.

Brightness and contrast
^^^^^^^^^^^^^^^^^^^^^^^

- Avoid unnecessary saturation when adjusting image display settings.
- If some saturation is unavoidable, make sure the displayed range still shows
  the structure that matters for interpretation.

Related pages
-------------

- :doc:`cloud-usage` for BioHPC access, Astrocyte uploads, and compute resource expectations
- :doc:`digital-tools` for account and platform setup
- :doc:`figure-preparation` for manuscript-ready figure formatting expectations
- :doc:`policies` for lab expectations that intersect with record keeping
