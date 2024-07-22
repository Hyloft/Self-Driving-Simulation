using UnityEngine;

public class PP : MonoBehaviour
{
    public Transform target; // The target point to follow
    public float lookAheadDistance = 5f; // Look-ahead distance

    private void Update()
    {
        // Calculate the target point
        Vector3 targetPoint = transform.position + transform.forward * lookAheadDistance;

        // Calculate the desired heading angle
        Vector3 toTarget = targetPoint - transform.position;
        float desiredAngle = Mathf.Atan2(toTarget.x, toTarget.z) * Mathf.Rad2Deg;

        // Calculate the steering angle
        float currentAngle = transform.eulerAngles.y;
        float steeringAngle = desiredAngle - currentAngle;
        print(steeringAngle);

        // Apply steering (you can use this angle to rotate the vehicle)
        // For example:
        transform.Rotate(Vector3.up, steeringAngle * Time.deltaTime);
        transform.Translate(Vector3.forward * 5 * Time.deltaTime);
    }
}