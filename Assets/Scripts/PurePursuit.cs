using UnityEngine;

public class PurePursuit : MonoBehaviour
{
    public Transform[] path; // Array of waypoints
    public float lookaheadDistance = 5.0f; // Lookahead distance
    public float velocity = 5.0f; // Car velocity

    private int currentWaypointIndex = 0;

    void Start()
    {
        if (path.Length < 2)
        {
            Debug.LogError("Path should have at least two waypoints.");
            return;
        }
    }

    void Update()
    {
        if (path.Length < 2)
        {
            return;
        }

        Vector3 currentPosition = transform.position;
        float currentAngle = transform.eulerAngles.y;

        Vector3 lookaheadPoint = FindLookaheadPoint(currentPosition);
        float steeringAngle = ComputeSteeringAngle(currentPosition, currentAngle, lookaheadPoint);

        // Apply the steering angle to the car
        transform.Rotate(Vector3.up, steeringAngle * Time.deltaTime);
        transform.Translate(Vector3.forward * velocity * Time.deltaTime);
    }

    Vector3 FindLookaheadPoint(Vector3 position)
    {
        for (int i = currentWaypointIndex; i < path.Length; i++)
        {
            float distance = Vector3.Distance(position, path[i].position);
            if (distance >= lookaheadDistance)
            {
                currentWaypointIndex = i;
                return path[i].position;
            }
        }
        return path[path.Length - 1].position;
    }

    float ComputeSteeringAngle(Vector3 position, float currentAngle, Vector3 lookaheadPoint)
    {
        Vector3 directionToLookaheadPoint = (lookaheadPoint - position).normalized;
        float angleToLookaheadPoint = Mathf.Atan2(directionToLookaheadPoint.z, directionToLookaheadPoint.x) * Mathf.Rad2Deg;

        float steeringAngle = angleToLookaheadPoint - currentAngle;

        // Normalize the steering angle to the range [-180, 180]
        if (steeringAngle > 180)
        {
            steeringAngle -= 360;
        }
        else if (steeringAngle < -180)
        {
            steeringAngle += 360;
        }

        return steeringAngle;
    }
}