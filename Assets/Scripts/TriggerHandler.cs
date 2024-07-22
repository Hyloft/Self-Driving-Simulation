using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TriggerHandler : MonoBehaviour
{
    // Settings
    [SerializeField] float reward;
    [SerializeField] bool reset;

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag != "Car") { return; }
        
        RewadController rc = other.gameObject.GetComponent<RewadController>();

        if (rc == null) {
            print("reward controller not found");
            return; 
        }

        if (reset) { rc.RestartSimulation(reward); }
        else { rc.AddTemporaryReward(reward); }
    }
}
