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

    # try to build model on calculating coefficient to change result reward
    # if car make serious mistakes it get minimum coefficient and result reward drops
    # max coefficient of each function can be optimized through learning
    MIN_COEFF = 0.05
    MAX_REWARD = 1.0
    ABS_STEERING_THRESHOLD = 15

    MAX_SPEED = 4.0
    MIN_SPEED = 1.0

    # if car on track
    def stay_on_track_coef():
        if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
            return 1.3
        return MIN_COEFF

    # if near to center line
    def follow_center_line_coef():
        closer_to_center = 0.1 * track_width
        allowed_distance = 0.25 * track_width
        close_to_off_track = 0.5 * track_width

        if distance_from_center <= closer_to_center:
            return 1.15
        elif distance_from_center <= allowed_distance:
            return 0.5
        elif distance_from_center <= close_to_off_track:
            return 0.2
        else:
            return MIN_COEFF

    # if car not zig-zag
    def abs_steering_coef():
        if abs(steering) > ABS_STEERING_THRESHOLD:
            return 0.8
        return 1.0

    # if car move with near maximum speed on straight line, while abs(steering) is minimum
    def moving_on_straight_line_faster_coef():
        if abs(steering) < 0.1:
            if round(speed) == MAX_SPEED:
                return 1.4
            elif round(speed) == MIN_SPEED:
                return 0.9
        elif abs(steering) < 0.2:
            if round(speed) == MAX_SPEED - 1:
                return 1.2
            elif round(speed) == MIN_SPEED:
                return 0.9

    # if car move to right turn based on waypoint and coordinates
    # if car move with calm speed on turns
    # if car end track with minimum steps

    reward = MAX_REWARD
    reward *= stay_on_track_coef()
    reward *= follow_center_line_coef()
    reward *= abs_steering_coef()
    reward *= moving_on_straight_line_faster_coef()

    return float(reward)
