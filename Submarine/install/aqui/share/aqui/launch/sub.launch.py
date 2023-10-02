import launch
import launch_ros.actions

def generate_launch_description():

    # Create a launch description object
    ld = launch.LaunchDescription()

    for i in range(100):
        node = launch_ros.actions.Node(
            package='aqui',
            executable='TestSub',
            name="b"+str(i),
            remappings=[("/a1","/a"+str(i))]
        )
        ld.add_action(node)

    return ld