using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using WebSocketSharp;
using static UnityEngine.GraphicsBuffer;

public class WSHandler : MonoBehaviour
{
    // WebSocket
    private WebSocket ws;
    private string url;

    // Settings
    [SerializeField] private KeyCode ssKey;
    [SerializeField] private bool sendAlways;
    [SerializeField] private bool sendCarXY;

    // Objects
    [SerializeField] private Camera _camera;
    [SerializeField] private GameObject car;
    
    // Controllers
    private RewadController rewadController;
    private CarController carController;

    void Start()
    {
        carController = car.GetComponent<CarController>();
        rewadController = car.GetComponent<RewadController>();

        url = "ws://localhost:8080/echo";
        ws = new WebSocket(url);
        ws.Connect();

        ws.OnMessage += (sender, e) =>
        {
            print("Message Received from " + ((WebSocket)sender).Url + ", Data : " + e.Data);
            CarMovementHandler(e.Data);
            SendReward(rewadController.GetCurrentReward());

        };

        _camera = _camera.GetComponent<Camera>();
        if (_camera.targetTexture == null)
        {
            _camera.targetTexture = new RenderTexture(640, 480, 24);
        }
        SendReward(rewadController.GetCurrentReward());

    }

    void Update()
    {
        print(GetTheta());
        if (ws == null)
        {
            return;
        }
        if (Input.GetKeyDown(ssKey) | sendAlways)
        {
            //ws.Send("Hello");
            CaptureAndSend();
        }
        if (sendCarXY)
        {
            SendCarCoords();
        }
    }

    private void CaptureAndSend()
    {
        RenderTexture activeRenderTexture = RenderTexture.active;
        Debug.Log(_camera);
        //print(_camera.targetTexture);
        RenderTexture.active = _camera.targetTexture;

        _camera.Render();

        Texture2D image = new Texture2D(_camera.targetTexture.width, _camera.targetTexture.height);
        image.ReadPixels(new Rect(0, 0, _camera.targetTexture.width, _camera.targetTexture.height), 0, 0);
        image.Apply();
        RenderTexture.active = activeRenderTexture;

        byte[] bytes = image.EncodeToPNG();
        Destroy(image);

        string b64s = Convert.ToBase64String(bytes);

        ws.Send("image:"+b64s);
    }

    public void SendReward(float reward)
    {
        ws.Send("reward:"+reward.ToString());
    }

    public void SendObstacle(float x,float y)
    {
        ws.Send("obstacle:" + $"{x}:{y}");
    }

    public float GetTheta()
    {
        Vector3 forward = transform.forward;

        // Calculate the angle in radians
        float angleRadians = Mathf.Atan2(forward.z, forward.x);

        // Convert the angle to degrees
        float angleDegrees = angleRadians * Mathf.Rad2Deg;

        // Adjust the angle to be clockwise (positive) and within the range [0, 360)
        angleDegrees = (angleDegrees) % 360;

        return angleDegrees;
    }

    public void SendCarCoords()
    {
        ws.Send("coords:" + $"{car.transform.position.x}:{car.transform.position.z}:{GetTheta()}");
    }
    private (float, float, float) MessageHandler(string input)
    {
        string[] values = input.Split(':');

        // Check if input has all required parts
        if (values.Length != 3)
        {
            print("Invalid input format. Please provide all values in the format '{speed}-{wheel}-{brake}'.");
        }

        if (!float.TryParse(values[0], out float speed) || !float.TryParse(values[1], out float wheel) || !float.TryParse(values[2], out float brake))
        {
            print("Invalid input format. Please provide numeric values.");
            return (0,0,0);
        }

        return (speed, wheel, brake);
    }

    private void CarMovementHandler(string msg)
    {
        (float speed, float wheel, float brake) = MessageHandler(msg);

        print("setting speed to:"+ speed+ " and wheel angle is:"+wheel);

        carController.SimulateWheel(speed, wheel, brake);
    }
}
