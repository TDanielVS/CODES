using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SendPosition : MonoBehaviour {

	
    public void SettingPosition(string pos)
    {
        GameObject.Find("persistent").SendMessage("SetPosition", pos);
    }

}
