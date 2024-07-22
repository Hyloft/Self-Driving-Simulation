using UnityEngine;

public class Lidar : MonoBehaviour
{
    [SerializeField] public float rayDistance = 15f; // The maximum distance of the raycast
    [SerializeField] private GameObject car;
    [SerializeField] private GameObject cam;

    private WSHandler handler;
    private SignalController controller;

    void Start()
    {
        handler = cam.GetComponent<WSHandler>();
        controller = car.GetComponent<SignalController>();
    }

    void Update()
    {
        int index = 0;
        for (int angle = -35; angle <= 35; angle += 10)
        {
            Vector3 direction = Quaternion.Euler(0, angle, 0) * transform.forward;

            RaycastHit hit;
            if (Physics.Raycast(transform.position, direction, out hit, rayDistance))
            {
                Vector3 hitPosition = hit.collider.gameObject.transform.position;
                Debug.Log("Hit point: " + hitPosition.x + ", " + hitPosition.z);
                handler.SendObstacle(hitPosition.x, hitPosition.z);

                // Draw debug line in the Scene view
                Debug.DrawLine(transform.position, hit.point, Color.red);
                Vector3 hitDirection = hit.point - transform.position;
                Vector3 crossProduct = Vector3.Cross(transform.forward, hitDirection);

                if (crossProduct.y > 0)
                {
                    Debug.Log("Hit point is on the right side: " + hit.point);
                    controller.StartBlinking(true);
                }
                else
                {
                    Debug.Log("Hit point is on the left side: " + hit.point);
                    controller.StartBlinking(false);
                }
            }
            else
            {
                // Update LineRenderer to show the laser reaching max distance
                Vector3 endPosition = transform.position + direction * rayDistance;
                Debug.DrawLine(transform.position, endPosition, Color.green);
            }
            index++;
        }
    }
}
