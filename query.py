# Query 

query1 = '''
query ($search: String) {
    Viewer {
        name
    }
    Page(perPage: 10) {
        media(search: $search, type: ANIME) {
        id
        title {
            userPreferred
        }

        airingSchedule {
            nodes {
            episode
            airingAt
            }
        }
    }
  }
}
'''
query2 = '''
query {
    Viewer {
        name
        id
    }
}
'''
query3 = '''
query ($userId: Int) {
    User (id: $userId) {
        name
    }
    MediaListCollection(userId: $userId, status: CURRENT, type: ANIME) {
        lists {
            entries {
                media {
                    id
                    title {
                        userPreferred
                    }
                }
            }
        }
    }
}

'''
query4 = '''
query ($mediaIds: [Int]) {
    Page {
        media(id_in: $mediaIds) {
            id
            title {
                userPreferred
            }
            status
            coverImage {
                medium
            }
            airingSchedule(perPage: 5, notYetAired: true) {
                nodes {
                    episode
                    airingAt
                    timeUntilAiring
                }
            }
        }
    }
}
'''
