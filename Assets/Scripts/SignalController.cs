using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SignalController : MonoBehaviour
{
    // Start is called before the first frame update
    [SerializeField] private Light left;
    [SerializeField] private Light right;
    [SerializeField] private GameObject car;
    [SerializeField] private int steer_angle = 20;

    public float blinkSpeed = 1.0f; // Speed of the blinking effect
    public float minIntensity = 0.0f; // Minimum intensity of the light
    public float maxIntensity = 1.0f; // Maximum intensity of the light
    public int blinkSec = 5; // Maximum intensity of the light

    private CarController controller;
    private Coroutine blinkCoroutine;
    void Start()
    {
        controller = car.GetComponent<CarController>();
        left.intensity = 0; right.intensity = 0;
    }

    // Update is called once per frame
    void Update()
    {
        left.intensity = 0; right.intensity = 0;
        if (Mathf.Abs(controller.steer_angle)>steer_angle)
        {
            if (controller.steer_angle < 0)
            {
                StartBlinking(true);
            }
            else
            {
                StartBlinking(false);
            }
        }
    }

    public void StartBlinking(bool isLeft)
    {
        if (blinkCoroutine != null)
        {
            StopCoroutine(blinkCoroutine);
        }
        Light l = isLeft ? left : right;
        blinkCoroutine = StartCoroutine(BlinkForSeconds(blinkSec, l));
    }

    private IEnumerator BlinkForSeconds(float duration,Light l)
    {
        float elapsedTime = 0.0f;

        while (elapsedTime < duration)
        {
            float intensity = (Mathf.Sin(Time.time * blinkSpeed) + 1.0f) / 2.0f; // Normalized to 0..1 range
            l.intensity = Mathf.Lerp(minIntensity, maxIntensity, intensity);

            elapsedTime += Time.deltaTime;
            yield return null;
        }

        // Reset the intensity to default value (optional)
        l.intensity = 0;
    }
}
