export const getStaticProps = async () => {
  return {
    redirect: {
      destination: "/community/contributor-guidelines",
      permanent: true,
    },
  };
};

const TestPage = () => {
  return <div></div>;
};

export default TestPage;
