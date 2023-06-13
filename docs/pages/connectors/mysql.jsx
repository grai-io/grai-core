export const getStaticProps = async () => {
  return {
    redirect: {
      destination: "/integrations/mysql",
      permanent: true,
    },
  };
};

const TestPage = () => {
  return <div></div>;
};

export default TestPage;
