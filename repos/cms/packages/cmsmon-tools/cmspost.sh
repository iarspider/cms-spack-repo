mkdir -p $RPM_INSTALL_PREFIX/cmsmon
./common_revision_script.sh .cmsmon-tools $RPM_INSTALL_PREFIX/cmsmon/.cmsmon-tools
for cmd in monit ggus_parser alert annotationManager nats-sub nats-pub dbs_vm promtool amtool prometheus hey stern trivy k8s_info gocurl ; do
  ln -sf .cmsmon-tools $RPM_INSTALL_PREFIX/cmsmon/$cmd
done
