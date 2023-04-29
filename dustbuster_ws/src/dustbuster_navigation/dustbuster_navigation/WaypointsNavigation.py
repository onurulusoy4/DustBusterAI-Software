import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav2_msgs.action import FollowWaypoints
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker, MarkerArray

class WaypointsNavigation(Node):

    def __init__(self):
        super().__init__('waypoints_navigation_node')
        self.subscription = self.create_subscription(
            String,
            'tsp_optimal_tour',
            self.waypoints_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.action_client = ActionClient(self, FollowWaypoints, 'follow_waypoints')
        self.waypoints = []
        self.marker_array_pub = self.create_publisher(MarkerArray, 'waypoints_markers', 10)
        self.marker_pub = self.create_publisher(MarkerArray, 'waypoints_labels', 10)

    def waypoints_callback(self, msg):
        data = msg.data.strip().split(';')
        for point in data:
            coords = point.split(',')
            x, y = float(coords[0].strip()), float(coords[1].strip())
            waypoint = PoseStamped()
            waypoint.header.frame_id = 'map'
            waypoint.pose.position.x = x
            waypoint.pose.position.y = y
            waypoint.pose.orientation.w = 1.0
            self.waypoints.append(waypoint)
            
            # Debug prints
            self.get_logger().info(f"Received waypoint: x={x}, y={y}")
            
        self.get_logger().info(f"Number of waypoints: {len(self.waypoints)}")
        self.publish_markers()
        self.publish_labels()
        self.send_navigation_goal()


    def send_navigation_goal(self):
        if not self.action_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('Action server not available.')
            return

        goal_msg = FollowWaypoints.Goal()
        goal_msg.poses = self.waypoints
        self.action_client.send_goal_async(goal_msg)

        self.get_logger().info('Sent navigation goal with waypoints.')
    
    def publish_markers(self):
        marker_array = MarkerArray()
        for idx, waypoint in enumerate(self.waypoints):
            marker = Marker()
            marker.header.frame_id = 'map'
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position.x = waypoint.pose.position.x
            marker.pose.position.y = waypoint.pose.position.y
            marker.pose.orientation.w = 1.0
            marker.id = idx
            marker.scale.x = 0.2
            marker.scale.y = 0.2
            marker.scale.z = 0.2
            marker.color.a = 1.0
            marker.color.r = 0.0
            marker.color.g = 1.0
            marker.color.b = 0.0
            marker_array.markers.append(marker)

        self.marker_array_pub.publish(marker_array)
    
    def publish_labels(self):
        marker_array = MarkerArray()

        for i, waypoint in enumerate(self.waypoints[:-1]):  # Exclude the last waypoint
            text_marker = Marker()
            text_marker.header.frame_id = 'map'
            text_marker.ns = 'waypoint_labels'
            text_marker.id = i
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.pose.position = waypoint.pose.position
            text_marker.pose.position.z += 0.5  # Adjust the height of the text label
            text_marker.pose.orientation.w = 1.0
            text_marker.scale.z = 0.3  # Adjust the size of the text
            text_marker.color.a = 1.0
            text_marker.color.r = 1.0
            text_marker.color.g = 1.0
            text_marker.color.b = 1.0
            text_marker.text = str(i + 1)  # Set the text to the waypoint index, add 1
            marker_array.markers.append(text_marker)

        self.marker_pub.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    waypoints_navigation_node = WaypointsNavigation()
    rclpy.spin(waypoints_navigation_node)

    waypoints_navigation_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
