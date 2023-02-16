const getRepoFromParams = (searchParams: URLSearchParams) => {
  const repository = searchParams.get("repository")
  const owner = repository && repository.split("/")[0]
  const repo = repository && repository?.split("/")[1]

  return { repo, owner }
}

export default getRepoFromParams
