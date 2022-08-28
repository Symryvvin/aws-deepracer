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

    MAX_SPEED = 2.0
    MIN_SPEED = 0.5
    ABS_STEERING_THRESHOLD = 15
    DIRECTION_THRESHOLD = 10.0
    
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
    
    # Low reward by default
    reward = 1e-3
    
    # Stay inside the two borders 
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
      reward = 1.0
    
    # Prevent Zig-Zag
    if abs(steering) > ABS_STEERING_THRESHOLD:
        reward *= 0.7
        
    # Penalty if speed is low    
    if speed < 1.3:
        reward *= 0.75
        
    # Right direction of car moving    
    next_wp = waypoints[closest_waypoints[1]]
    prev_wp = waypoints[closest_waypoints[0]]

    direction_diff = abs(track_heading(prev_wp, next_wp) - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.4
        
    next_wp_index = closest_waypoints[1]
    first_angle = track_heading(wp_by_index(next_wp_index), wp_by_index(next_wp_index + 5))
    second_angle = track_heading(wp_by_index(next_wp_index), wp_by_index(next_wp_index - 5))

    turn_angle = first_angle - second_angle

    if (turn_angle > 0 and is_left_of_center) or (turn_angle < 0 and not is_left_of_center):
      reward *= 1.3

    return float(reward)
