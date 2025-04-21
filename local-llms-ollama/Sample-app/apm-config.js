// apm-config.js
import { init as initApm } from '@elastic/apm-rum';

var apm = initApm({
  serviceName: 'my-service-name',
  serverUrl: 'https://aa14675c565c4437b58187566bcfc11c.apm.ap-south-1.aws.elastic-cloud.com:443',
  serviceVersion: '',
  environment: 'my-environment'
});

export default apm;
