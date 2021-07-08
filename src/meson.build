python = import('python')
python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'singral.in',
  output: 'singral',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

singral_sources = [
  'main.py',
]

install_data(singral_sources, install_dir: moduledir)
install_subdir('api', install_dir: moduledir)
install_subdir('widgets', install_dir: moduledir)
