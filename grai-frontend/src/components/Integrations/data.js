import React from 'react'
import {
  AzureIcon,
  KafkaIcon,
  AWSIcon,
  AwsSqsIcon,
  AWSSNSIcon,
  RabbitMQIcon,
  MQTTIcon,
  ActiveMQIcon,
  PulsarIcon,
  AzureServiceBusIcon,
  AzureEventBusIcon,
  NatsIcon,
  RedisIcon,
  PostgresIcon,
  MongoDBIcon, AWSKinesisIcon
} from "./icons"


export const Data = {
  integrations: [
    {
      label: 'Kafka',
      bg: '#E6E5E5',
      icon: <KafkaIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'RabbitMQ',
      bg: '#FFE8DC',
      icon: <RabbitMQIcon h={["35px", null, null, "45px"]} />,
    },
    {
      label: 'MQTT',
      bg: '#D9BFD9',
      icon: <MQTTIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'AWS',
      bg: '#FFEDD1',
      icon: <AWSIcon h={["29px", null, null, "35px"]} marginTop={["5px", null, null, "10px"]}/>
    },
    {
      label: 'AWS Kinesis',
      bg: '#FFE4BB',
      icon: <AWSKinesisIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'AWS SQS',
      bg: '#F2E2C0',
      icon: <AwsSqsIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'AWS SNS',
      bg: '#EBD3DF',
      icon: <AWSSNSIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'ActiveMQ',
      bg: '#E7ECD9',
      icon: <ActiveMQIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'Pulsar',
      bg: '#D1E9FF',
      icon: <PulsarIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'Azure',
      bg: '#CCE3F4',
      icon: <AzureIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'Service Bus',
      bg: '#D4E4FF',
      icon: <AzureServiceBusIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'Event Bus',
      bg: '#CCE2F6',
      icon: <AzureEventBusIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'NATS',
      bg: '#E8F4D9',
      icon: <NatsIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'Redis',
      bg: '#F7D5D2',
      icon: <RedisIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'Postgres',
      bg: '#D6E1E9',
      icon: <PostgresIcon h={["35px", null, null, "45px"]} />
    },
    {
      label: 'MongoDB',
      bg: '#DCEED9',
      icon: <MongoDBIcon h={["35px", null, null, "45px"]} />
    }
  ]
}