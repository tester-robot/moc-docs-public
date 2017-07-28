// jaeger-openshift

github: https://github.com/jaegertracing/jaeger-openshift


c login -u system:admin
oc new-project jaeger
oc process -f https://raw.githubusercontent.com/jaegertracing/jaeger-openshift/master/production/jaeger-production-template.yml | oc create -n jaeger -f -

oc policy add-role-to-user cluster-admin developer -n jaeger