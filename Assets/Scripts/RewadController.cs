using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class RewadController : MonoBehaviour
{
    // Needed Objects
    [SerializeField] private Camera _camera;
    [SerializeField] private GameObject car;
    [SerializeField] private GameObject middleObject; // the middle of the road
    
    // Controllers
    private WSHandler ws;
    private CarController carController;
    
    // Variables
    private float currentReward;
    private float temporaryReward;
    private float startTime;
    
    void Start()
    {
        ws = _camera.GetComponent<WSHandler>();
        carController = car.GetComponent<CarController>();
        startTime = Time.time;
    }

    void Update()
    {
        // you can define your reward changes on update right here
        currentReward = GetTimeReward() + GetDistenceReward();

    }

    public float GetCurrentReward()
    {
        float rewardCumulative = currentReward+temporaryReward;
        temporaryReward = 0;
        return rewardCumulative;
    }

    public void AddTemporaryReward(float reward)
    {
        temporaryReward += reward;
    }

    public void RestartSimulation(float reward)
    {
        carController.ResetCar();
        AddTemporaryReward(reward);
    }
    
    private float GetTimeReward()
    {
        startTime = Time.time;
        return startTime - Time.time;
    }

    private float GetDistenceReward() // not sure about that
    {
        return -1 * Mathf.Abs(carController.car.transform.position.x - middleObject.transform.position.x);
    }

}
