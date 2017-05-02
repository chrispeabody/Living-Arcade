using UnityEngine;
using System.Collections;

public class ObjController : MonoBehaviour
{
    public string gameURL = "http://149.56.28.102/display.php&ID=";
    public string response;

    void Start()
    {
        string ID = "282931167881809444187161050873593334202";
        StartCoroutine(GetScores(ID));
    }

    IEnumerator GetScores(string ID)
    {
        WWW obj_get = new WWW(gameURL + ID);
        yield return obj_get;

        if (obj_get.error != null)
        {
            print("There was an error getting the objects: " + obj_get.error);
        }
        else
        {
            response = obj_get.text;
            print(response);
        }
    }

}
