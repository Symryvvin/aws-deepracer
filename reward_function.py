def reward_function(params):

    # x and y  - The position of the vehicle on the track
    # heading - Orientation of the vehicle on the track
    # waypoints - List of waypoint coordinates
    # closest_waypoints - Index of the two closest waypoints to the vehicle
    # progress - Percentage of track completed
    # steps - Number of steps completed
    # track_width - Width of the track
    # distance_from_center - Distance from track center line
    # is_left_of_center - Whether the vehicle is to the left of the center line
    # all_wheels_on_track - Is the vehicle completely within the track boundary?
    # speed - Observed speed of the vehicle
    # steering_angle - Steering angle of the front wheels

    coordinates = [params['x'], params['y']]
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    progress = params['progress']
    steps = params['steps']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steering = params['steering_angle']

    NO_REWARD = 0
    MAX_REWARD = 1.0

    reward = NO_REWARD

    return float(reward)
