import math


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

    MIN_REWARD = 1e-3
    MAX_REWARD = 1.0

    MAX_SPEED = 3.0
    MIN_SPEED = 0.5

    def stay_car_on_track():
        if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
            return MAX_REWARD * 1.3
        return MIN_REWARD

    def follow_near_center_track_line():
        closer_to_center = 0.1 * track_width
        allowed_distance = 0.25 * track_width
        close_to_off_track = 0.5 * track_width

        if distance_from_center <= closer_to_center:
            return MAX_REWARD * 1.1
        elif distance_from_center <= allowed_distance:
            return MAX_REWARD * 0.5
        elif distance_from_center <= close_to_off_track:
            return MAX_REWARD * 0.2
        else:
            return MIN_REWARD

    def abs_steering():
        ABS_STEERING_THRESHOLD = 15

        if abs(steering) > ABS_STEERING_THRESHOLD:
            return MAX_REWARD * 0.8
        return MAX_REWARD

    def moving_on_straight_line_faster():
        if abs(steering) < 0.1:
            if round(speed) == MAX_SPEED:
                return MAX_REWARD * 1.4
            elif round(speed) == MIN_SPEED:
                return MAX_REWARD * 0.9
        # elif abs(steering) < 0.2:
        #     if round(speed) == MAX_SPEED - 1:
        #         return MAX_REWARD * 1.2
        #     elif round(speed) == MIN_SPEED:
        #         return MAX_REWARD * 0.9
        return MAX_REWARD

    def track_heading(prev_wp, next_wp):
        track_heading_in_rads = math.atan2(next_wp[1] - prev_wp[1], next_wp[0] - prev_wp[0])
        return math.degrees(track_heading_in_rads)

    def wp_by_index(index):
        if index > (len(waypoints) - 1):
            return waypoints[index - (len(waypoints))]
        elif index < 0:
            return waypoints[len(waypoints) + index]
        else:
            return waypoints[index]

    def track_turn_angle(next_wp_index):
        first_angle = track_heading(wp_by_index(next_wp_index), wp_by_index(next_wp_index + 1))
        second_angle = track_heading(wp_by_index(next_wp_index), wp_by_index(next_wp_index - 1))

        return first_angle - second_angle

    def left_of_center_when_turn():
        next_wp_index = closest_waypoints[1]
        turn_angle = track_turn_angle(next_wp_index)

        if turn_angle > 0:
            if is_left_of_center:
                return MAX_REWARD * 1.2
            else:
                return MAX_REWARD * 0.7
        elif turn_angle < 0:
            if is_left_of_center:
                return MAX_REWARD * 0.7
            else:
                return MAX_REWARD * 1.2

        return MAX_REWARD

    def slow_speed_when_turn():
        next_wp = closest_waypoints[1]
        abs_turn_angle = abs(track_turn_angle(next_wp))

        if abs_turn_angle > 20 and MAX_SPEED - 1 > speed > MIN_SPEED + 1:
            return MAX_REWARD * 1.2
        elif abs_turn_angle > 40 and MAX_SPEED - 2 > speed > MIN_SPEED + 0.5:
            return MAX_REWARD * 1.2
        return MAX_REWARD

    def car_move_in_right_direction():
        next_wp = waypoints[closest_waypoints[1]]
        prev_wp = waypoints[closest_waypoints[0]]

        direction_diff = abs(track_heading(prev_wp, next_wp) - heading)
        if direction_diff > 180:
            direction_diff = 360 - direction_diff

        DIRECTION_THRESHOLD = 10.0
        if direction_diff > DIRECTION_THRESHOLD:
            return MAX_REWARD * 0.5

        return MAX_REWARD

    reward = stay_car_on_track()
    reward += follow_near_center_track_line()
    reward += abs_steering()
    reward += left_of_center_when_turn()
    reward += slow_speed_when_turn()
    reward += car_move_in_right_direction()
    reward += moving_on_straight_line_faster()

    return float(reward)
