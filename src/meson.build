pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'cuneo'
gnome = import('gnome')

gnome.compile_resources('cuneo',
  'cuneo.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'cuneo.in',
  output: 'cuneo',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

cuneo_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'units.py',
  'conversion.py',
  'token.py',
  'magic.py',
  'history_window.py',
  'conversion_stack.py',
  'calculation_stack.py'
]



install_data(cuneo_sources, install_dir: moduledir)
