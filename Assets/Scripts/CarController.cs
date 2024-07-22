using System;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class CarController : MonoBehaviour
{
    // Inputs
    [NonSerialized] private float horizontalInput, verticalInput;
    [NonSerialized] private float currentSteerAngle, currentbreakForce;
    [NonSerialized] private bool isBreaking;
    [NonSerialized] private float maxSteerAngle;

    // Settings
    [SerializeField] private float motorForce, breakForce;
    [SerializeField] private bool UnityControl;
    [SerializeField] private float maxSpeed = 100f;  // Add this line

    // Wheel Colliders
    [SerializeField] private WheelCollider frontLeftWheelCollider, frontRightWheelCollider;
    [SerializeField] private WheelCollider rearLeftWheelCollider, rearRightWheelCollider;

    // Wheels
    [SerializeField] private Transform frontLeftWheelTransform, frontRightWheelTransform;
    [SerializeField] private Transform rearLeftWheelTransform, rearRightWheelTransform;

    // Variables
    public GameObject car;
    private Vector3 positionStart;
    Vector3 eulerRotationStart;
    public float steer_angle;

    private void Start()
    {
        car = gameObject;
        positionStart = transform.position;
        eulerRotationStart = new Vector3(transform.eulerAngles.x, transform.eulerAngles.y, transform.eulerAngles.z);
        maxSteerAngle = 45;
        steer_angle = 0;
    }

    private void FixedUpdate() {
        if (UnityControl) GetInput(); // to control in unity
        HandleMotor();
        HandleSteering();
        UpdateWheels();
        steer_angle = maxSteerAngle * horizontalInput;
    }

    private void GetInput() {
        // Steering Input
        horizontalInput = Input.GetAxis("Horizontal");

        // Acceleration Input
        verticalInput = Input.GetAxis("Vertical");

        // Breaking Input
        isBreaking = Input.GetKey(KeyCode.Space);
    }

    private void HandleMotor()
    {
        Rigidbody rb = GetComponent<Rigidbody>();
        if (rb.velocity.magnitude < maxSpeed) // Check current speed
        {
            frontLeftWheelCollider.motorTorque = verticalInput * motorForce;
            frontRightWheelCollider.motorTorque = verticalInput * motorForce;
        }
        else
        {
            frontLeftWheelCollider.motorTorque = 0;
            frontRightWheelCollider.motorTorque = 0;
        }
        currentbreakForce = isBreaking ? breakForce : 0f;
        ApplyBreaking();
    }

    private void ApplyBreaking() {
        frontRightWheelCollider.brakeTorque = currentbreakForce;
        frontLeftWheelCollider.brakeTorque = currentbreakForce;
        rearLeftWheelCollider.brakeTorque = currentbreakForce;
        rearRightWheelCollider.brakeTorque = currentbreakForce;
    }

    private void HandleSteering() {
        currentSteerAngle = maxSteerAngle * horizontalInput;
        frontLeftWheelCollider.steerAngle = currentSteerAngle;
        frontRightWheelCollider.steerAngle = currentSteerAngle;
    }

    private void UpdateWheels() {
        UpdateSingleWheel(frontLeftWheelCollider, frontLeftWheelTransform);
        UpdateSingleWheel(frontRightWheelCollider, frontRightWheelTransform);
        UpdateSingleWheel(rearRightWheelCollider, rearRightWheelTransform);
        UpdateSingleWheel(rearLeftWheelCollider, rearLeftWheelTransform);
    }

    private void UpdateSingleWheel(WheelCollider wheelCollider, Transform wheelTransform) {
        Vector3 pos;
        Quaternion rot; 
        wheelCollider.GetWorldPose(out pos, out rot);
        wheelTransform.rotation = rot;
        wheelTransform.position = pos;
    }

    public void SimulateWheel(float speed, float wheel, float brake)
    {
        if (UnityControl) return;
        isBreaking = brake > 0 ? true : false;
        verticalInput = speed;
        horizontalInput = wheel > 0 ? 1 : (wheel < 0 ? -1 : 0);
        maxSteerAngle = Math.Abs(wheel);
    }

    public void ResetCar()
    {
        transform.rotation = Quaternion.Euler(eulerRotationStart);
        transform.position = positionStart;
        frontLeftWheelCollider.motorTorque = 0;
        frontRightWheelCollider.motorTorque = 0;
        Rigidbody rb = GetComponent<Rigidbody>();
        rb.velocity = Vector3.zero;
        rb.angularVelocity = Vector3.zero;
        horizontalInput = 0;
        verticalInput = 0;
        isBreaking = true;
    }
}