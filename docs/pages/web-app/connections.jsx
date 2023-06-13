export const getStaticProps = async () => {
  return {
    redirect: {
      destination: "/integrations/support-status",
      permanent: true,
    },
  };
};

const TestPage = () => {
  return <div></div>;
};

export default TestPage;
