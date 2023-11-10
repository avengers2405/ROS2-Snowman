#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist #bcz this is needed by the topic
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from functools import partial
#add to the dependencies

class DrawCicrle(Node):
    def __init__(self):
        super().__init__("draw_cirlce")
        self.half_circle=False
        self.stop_turtle=False
        self.circle1_complete=False
        self.turtle2_start=False
        self.init_x=0
        self.init_y=0
        self.took_init_pos=False
        self.kid_turtle_half=False
        self.kid_turtle_stop=False
        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10) #create publisher
        self.cmd_vel_pub2 = self.create_publisher(Twist, "/kid_turtle/cmd_vel", 10) #create publisher
        #args: Twist used, publisher name, queue (to creat ebuffer to send commands if it gets too long or transmission inefficiency is there)
        #if not self.circle1_complete:
        self.reciever_feedback = self.create_subscription(Pose, "/turtle1/pose", self.callback_feedback, 10)
        #else:
        self.reciever_feedback2 = self.create_subscription(Pose, "/kid_turtle/pose", self.callback_feedback2, 10)
        #self.timer_ = self.create_timer(0.5, self.send_vel_cmd)
        #timer will call it every 0.5 seconds
        self.get_logger().info("Circle has started")
        self.get_logger().info("Code updated")

    def spawn_service(self, x, y, theta, name): #service /spawn takes x, y coords and theta, and name (optional)
        client = self.create_client(Spawn, "/spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service server to be ON")
        
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = "kid_turtle"

        future = client.call_async(request)
        future.add_done_callback(partial(self.service_callback))
    
    def service_callback(self, future):
        response = future.result()

    def callback_feedback2(self, msg2: Pose):
        msg=Twist()
        if not self.kid_turtle_stop:
            self.get_logger().info("second turtle spawned")
            if msg2.theta>0:
                self.get_logger().info("positive")
                self.kid_turtle_half=True
            if self.kid_turtle_half:
                self.get_logger().info("next loop in tandem")
                if msg2.theta<0:
                    self.get_logger().info("Last iteration, expected")
                    self.kid_turtle_stop=True
                    msg.linear.x=0.0
                    msg.angular.z=0.0
                    self.get_logger().info("Publishing 0 speed and 0 angular velc.")
                    self.cmd_vel_pub2.publish(msg)
        
        if not self.kid_turtle_stop:
            self.get_logger().info("x: "+str(msg2.x)+"y: "+str(msg2.y)+"theta: "+str(msg2.theta))
            self.get_logger().info("Publishing speeed for kid turtle")
            msg.linear.x = 2.0
            msg.angular.z = -1.0
            self.cmd_vel_pub2.publish(msg)
        else:
            msg.linear.x=0.0
            msg.angular.z=0.0
            self.get_logger().info("Publishing 0 speed and 0 angular velc.")
            self.cmd_vel_pub2.publish(msg)

    def callback_feedback(self, msg2: Pose):
        self.get_logger().info("Feedbak is being called")
        if not self.took_init_pos:
            self.init_x=msg2.x
            self.init_y=msg2.y
            self.took_init_pos=True
        msg=Twist()
        if not self.stop_turtle:
            self.get_logger().info(str(msg2.theta))
            if msg2.theta<0:
                self.get_logger().info("theta is negative rn")
                self.half_circle=True
            if self.half_circle:
                self.get_logger().info("Atleast get here bro")
                if msg2.theta>0:
                    #self.get_logger().info("Here only when one full circle is completed.")
                    self.stop_turtle=True
                    msg.linear.x=0.0
                    msg.angular.z=0.0
                    #self.get_logger().info("Publishing 0 speed and 0 angular velc.")
                    self.cmd_vel_pub.publish(msg)
                    #self.get_logger().info("Spawning 2nd turtle")
                    self.spawn_service(self.init_x, self.init_y, 0.0, "kid_turtle")
                    self.turtle2_start=True
                    #self.reciever_feedback.destroy()

        if not self.stop_turtle:
            self.get_logger().info("Publishing speeed")
            msg.linear.x = 1.0
            msg.angular.z = 1.0
            self.cmd_vel_pub.publish(msg)
        else:
            msg.linear.x=0.0
            msg.angular.z=0.0
            self.get_logger().info("x: "+str(msg2.x)+"y: "+str(msg2.y)+"theta: "+str(msg2.theta))
            self.cmd_vel_pub.publish(msg)
            

    '''def send_vel_cmd(self):
        msg = Twist()
        if not self.stop_turtle:
            self.get_logger().info("Publishing speeed")
            msg.linear.x = 2.0
            msg.angular.z = 1.0
            self.cmd_vel_pub.publish(msg) # publishes the msg with our info to reuqred topic declared before
        else:
            self.get_logger().info("Publishing 0 speed and 0 angular velc.")
            msg.linear.x=0.0
            msg.angular.z=0.0
            self.cmd_vel_pub.publish(msg)'''

def main(args=None):
    rclpy.init(args=args)
    node = DrawCicrle()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()