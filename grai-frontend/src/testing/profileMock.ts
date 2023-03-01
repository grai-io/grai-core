import { GET_PROFILE } from "components/layout/ProfileMenu"

const profileMock = {
  request: {
    query: GET_PROFILE,
  },
  result: {
    data: {
      profile: {
        id: "1",
        username: "test@example.com",
        first_name: "Test",
        last_name: "Example",
      },
    },
  },
}

export default profileMock
