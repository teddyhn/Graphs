import random

class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class SocialGraph:
    def __init__(self):
        self.called_add_friendship = 0
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """

        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
            return False
        else:
            self.called_add_friendship += 1
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments
        Creates that number of users and a randomly distributed friendships
        between those users.
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # # Add users
        for i in range(num_users):
            self.add_user(f'User {i + 1}')

        target_friendships = (num_users * avg_friendships)
        total_friendships = 0

        while total_friendships < target_friendships:
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)

            if self.add_friendship(user_id, friend_id):
                total_friendships += 2

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """
        # DO BFT and store the paths along the way

        queue = Queue()
        visited = {}  # Note that this is a dictionary, not a set

        queue.enqueue([user_id])

        while queue.size() > 0:
            path = queue.dequeue()
            current_friend = path[-1]

            if current_friend not in visited:
                visited[current_friend] = path
                path_copy = path.copy()

                for friend_id in self.friendships[current_friend]:
                    path_copy.append(friend_id)
                    queue.enqueue(path_copy)

        return visited

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


if __name__ == '__main__':
    sg = SocialGraph()
    # sg.populate_graph(100, 10)
    # Question 1: 500 times

    sg.populate_graph(1000, 5)

    print(sg.called_add_friendship)
    print(sg.friendships)
    avg_degree_separation = 0

    for i in range(1, len(sg.users) + 1):
        connections = sg.get_all_social_paths(i)
        degrees_separation = 0
        for k in connections:
            degrees_separation += len(connections[k])
        avg_degree_separation += degrees_separation / len(connections)

    extended_network = 0

    for i in range(1, len(sg.users) + 1):
        connections = sg.get_all_social_paths(i)
        for k in connections:
            extended_network += len(connections[k]) - 1
    
    avg_extended_network = extended_network / len(sg.users)


    # Question 2:
    print(f'Percentage of users in extended network: {avg_extended_network}')
    print(f'Average degree of separation: {avg_degree_separation / len(sg.users)}')
    print(connections)
